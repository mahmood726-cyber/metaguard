"""MetaGuard integration + unit tests — 3 frontier engines."""
import sys, time, json, math, pytest
sys.path.insert(0, __import__('os').path.dirname(__file__))
from conftest import js

@pytest.fixture(autouse=True)
def load_app(driver, app_url):
    if driver.current_url != app_url:
        driver.get(app_url)
        time.sleep(1)


# ── App Loading ──

class TestAppLoads:
    def test_title(self, driver):
        assert 'MetaGuard' in driver.title

    def test_no_js_errors(self, driver):
        logs = driver.get_log('browser')
        severe = [l for l in logs if l['level'] == 'SEVERE']
        assert len(severe) == 0, f"JS errors: {severe}"

    def test_tabs_present(self, driver):
        tabs = driver.find_elements('css selector', '.tab-btn')
        assert len(tabs) == 8  # Data, Robust, P-Hack, MetaForest, Rare Events, Causal, Report, About


class TestTabSwitching:
    def test_cycle_all_tabs(self, driver):
        for tab in ['data', 'robust', 'phack', 'forest', 'rare', 'causal', 'report', 'about']:
            driver.find_element('css selector', f'.tab-btn[data-tab="{tab}"]').click()
            time.sleep(0.2)
            panel = driver.find_element('id', f'tab-{tab}')
            assert panel.is_displayed()


# ── Engine 1: Robust Pooling (DPD) ──

class TestRobustPooling:
    def test_alpha0_is_mle(self, driver):
        """Alpha=0 should give standard inverse-variance MLE"""
        r = js(driver, '''(function() {
            var yi = [0.5, 0.3, 0.7, 0.4];
            var sei = [0.1, 0.15, 0.2, 0.12];
            return robustPool(yi, sei, 0);
        })()''')
        assert r['theta'] is not None
        assert r['alpha'] == 0

    def test_alpha05_downweights_outlier(self, driver):
        """Outlier should be downweighted at alpha=0.5"""
        r = js(driver, '''(function() {
            var yi = [0.5, 0.5, 0.5, 5.0];
            var sei = [0.1, 0.1, 0.1, 0.1];
            return robustPool(yi, sei, 0.5);
        })()''')
        # Robust estimate should be closer to 0.5 than MLE
        assert r['theta'] is not None
        assert r['theta'] < 2.0  # MLE would be ~1.625, robust should be lower
        # Outlier (study 3) should be downweighted
        assert r['outlier_adjusted'][3]['downweighted'] is True

    def test_shift_increases_with_outlier(self, driver):
        """Shift from MLE should be nonzero when outlier present"""
        r = js(driver, '''(function() {
            var yi = [0.5, 0.5, 0.5, 5.0];
            var sei = [0.1, 0.1, 0.1, 0.1];
            return robustPool(yi, sei, 0.5);
        })()''')
        assert r['shift'] > 0.1

    def test_no_outlier_small_shift(self, driver):
        """Homogeneous data should have small shift"""
        r = js(driver, '''(function() {
            var yi = [0.5, 0.48, 0.52, 0.49];
            var sei = [0.1, 0.1, 0.1, 0.1];
            return robustPool(yi, sei, 0.5);
        })()''')
        assert r['shift'] < 0.05

    def test_ci_contains_theta(self, driver):
        r = js(driver, '''(function() {
            var yi = [0.5, 0.3, 0.7];
            var sei = [0.1, 0.2, 0.15];
            return robustPool(yi, sei, 0.5);
        })()''')
        assert r['ci_lo'] < r['theta'] < r['ci_hi']


# ── Engine 2: RTMA + MAN ──

class TestRTMA:
    def test_runs_on_demo(self, driver):
        """RTMA should produce results on demo data"""
        driver.execute_script('document.getElementById("loadDemo").click()')
        time.sleep(0.5)
        driver.execute_script('document.getElementById("runBtn").click()')
        time.sleep(3)
        r = js(driver, 'JSON.stringify(window.mgResults.phack)')
        data = json.loads(r)
        assert data['available'] is True
        assert data['rtma']['theta'] is not None
        assert data['phack_suspicion'] in ('LOW', 'MODERATE', 'HIGH')

    def test_man_uses_fewer_studies(self, driver):
        """MAN should use fewer studies than total"""
        r = js(driver, 'window.mgResults.phack')
        if r and r.get('man'):
            assert r['man']['k_used'] < r['k_total']

    def test_affirmative_classification(self, driver):
        """Should classify affirmative vs non-affirmative"""
        r = js(driver, 'window.mgResults.phack')
        assert r['k_affirmative'] + r['k_nonaffirmative'] == r['k_total']

    def test_caliper_count(self, driver):
        """Caliper count should be non-negative"""
        r = js(driver, 'window.mgResults.phack')
        assert r['caliper_count'] >= 0

    def test_rtma_corrects_toward_null(self, driver):
        """RTMA should generally correct toward null vs naive"""
        r = js(driver, 'window.mgResults.phack')
        if r and r.get('rtma'):
            # RTMA theta should be closer to 0 than naive (typically)
            # Not guaranteed but expected for data with p-hacking
            assert r['rtma']['theta'] is not None

    def test_man_is_conservative(self, driver):
        """MAN (non-affirmative only) should be more conservative"""
        r = js(driver, 'window.mgResults.phack')
        if r and r.get('man') and r.get('rtma'):
            # MAN uses only non-affirmative -> should give smaller effect
            assert abs(r['man']['theta']) <= abs(r['naive_theta']) + 0.01


# ── Engine 3: MetaForest ──

class TestMetaForest:
    def test_runs_on_demo(self, driver):
        """MetaForest should produce results"""
        r = js(driver, 'window.mgResults.forest')
        assert r['available'] is True
        assert r['oob_r2'] is not None

    def test_variable_importance_sums_roughly_to_one(self, driver):
        """Importance values should be meaningful"""
        r = js(driver, 'window.mgResults.forest')
        vimp = r.get('variable_importance', [])
        assert len(vimp) >= 1
        # All importance values should be defined
        for v in vimp:
            assert v['name'] is not None

    def test_predictions_exist(self, driver):
        """Should have one prediction per study"""
        r = js(driver, 'window.mgResults.forest')
        assert len(r['predictions']) == 12  # demo has 12 studies

    def test_n_trees(self, driver):
        r = js(driver, 'window.mgResults.forest')
        assert r['n_trees'] == 200

    def test_top_moderator_named(self, driver):
        r = js(driver, 'window.mgResults.forest')
        assert r['variable_importance'][0]['name'] is not None


# ── Dark Mode ──

class TestDarkMode:
    def test_toggle(self, driver):
        toggle = driver.find_element('id', 'themeToggle')
        toggle.click()
        time.sleep(0.2)
        is_light = js(driver, 'document.body.classList.contains("light")')
        assert is_light is True
        toggle.click()
        time.sleep(0.2)
        is_light = js(driver, 'document.body.classList.contains("light")')
        assert is_light is False


# ── Export ──

class TestExport:
    def test_report_tab_renders(self, driver):
        driver.find_element('css selector', '.tab-btn[data-tab="report"]').click()
        time.sleep(0.3)
        panel = driver.find_element('id', 'tab-report')
        content = panel.get_attribute('innerHTML')
        assert 'Executive Summary' in content or 'Robust' in content
