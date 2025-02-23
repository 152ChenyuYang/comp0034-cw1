import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time


class TestDashboard:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        """Set up the test environment before each test"""
        try:
            # Configure Chrome options
            chrome_options = Options()
            # chrome_options.add_argument('--headless')
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")  # Set window size

            service = Service(ChromeDriverManager().install())

            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            self.driver.get("http://localhost:5050")

            self.wait = WebDriverWait(self.driver, 20)  # Increased wait time
            time.sleep(2)

            yield

        except Exception as e:
            pytest.fail(f"Failed to setup ChromeDriver: {str(e)}")

        finally:
            if hasattr(self, "driver"):
                self.driver.quit()

    def test_page_title(self):
        """Test if the page title is correctly displayed"""
        title = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Housing Supply & Demand')]")
            )
        )
        assert title.is_displayed()
        assert "Housing Supply & Demand Visualization" in title.text

    def test_chart_visibility(self):
        """Test if all charts are visible on the page"""
        time.sleep(3)
        line_chart = self.wait.until(
            EC.presence_of_element_located((By.ID, "waiting-line-chart"))
        )
        assert line_chart.is_displayed()

        bar_chart = self.wait.until(
            EC.presence_of_element_located((By.ID, "housing-bar-chart"))
        )
        assert bar_chart.is_displayed()

        map_chart = self.wait.until(
            EC.presence_of_element_located((By.ID, "housing-map"))
        )
        assert map_chart.is_displayed()

        pie_chart = self.wait.until(
            EC.presence_of_element_located((By.ID, "housing-pie-chart"))
        )
        assert pie_chart.is_displayed()

    def test_area_dropdown_functionality(self):
        """Test if the area codes dropdown works correctly"""
        try:
            dropdown_container = self.wait.until(
                EC.presence_of_element_located((By.ID, "area-dropdown"))
            )
            assert (
                dropdown_container.is_displayed()
            ), "Dropdown container should be visible"

            select_control = dropdown_container.find_element(
                By.CLASS_NAME, "Select-control"
            )
            select_control.click()
            time.sleep(1)

            dropdown_options = self.driver.find_elements(
                By.CLASS_NAME, "VirtualizedSelectOption"
            )
            assert len(dropdown_options) > 0, "Dropdown should have options"

            second_option = dropdown_options[1]
            second_option_text = second_option.text
            second_option.click()
            time.sleep(2)

            selected_values = self.driver.find_elements(
                By.CLASS_NAME, "Select-value-label"
            )
            assert len(selected_values) == 4, "Should have 4 selected values"

            charts = [
                "waiting-line-chart",
                "housing-bar-chart",
                "housing-map",
                "housing-pie-chart",
            ]

            for chart_id in charts:
                chart = self.wait.until(
                    EC.presence_of_element_located((By.ID, chart_id))
                )
                assert chart.is_displayed(), f"{chart_id} should be visible"

            # Test removing a selection
            close_buttons = self.driver.find_elements(
                By.CLASS_NAME, "Select-value-icon"
            )
            close_buttons[0].click()
            time.sleep(1)

            # Verify only one selection remains
            remaining_values = self.driver.find_elements(
                By.CLASS_NAME, "Select-value-label"
            )
            assert len(remaining_values) == 3, "Should have 3 remaining value"

        except Exception as e:
            pytest.fail(f"Area dropdown test failed: {str(e)}")

    def test_data_type_dropdowns(self):
        """Test if the data type dropdowns for line and bar charts work correctly"""
        try:
            line_dropdown = self.wait.until(
                EC.presence_of_element_located((By.ID, "line-data-dropdown"))
            )
            assert (
                line_dropdown.is_displayed()
            ), "Line chart data type dropdown should be visible"

            line_select = line_dropdown.find_element(By.CLASS_NAME, "Select-control")
            line_select.click()
            time.sleep(1)

            line_options = self.driver.find_elements(
                By.CLASS_NAME, "VirtualizedSelectOption"
            )
            assert len(line_options) > 0, "Line chart dropdown should have options"

            # Select Percentage Change option
            for option in line_options:
                if option.text == "Percentage Change":
                    option.click()
                    break
            time.sleep(2)
            line_selected = line_dropdown.find_element(
                By.CLASS_NAME, "Select-value-label"
            )
            assert (
                line_selected.text == "Percentage Change"
            ), "Line chart should show Percentage Change"

            # Test bar chart data type dropdown
            bar_dropdown = self.wait.until(
                EC.presence_of_element_located((By.ID, "bar-data-dropdown"))
            )
            assert (
                bar_dropdown.is_displayed()
            ), "Bar chart data type dropdown should be visible"

            bar_select = bar_dropdown.find_element(By.CLASS_NAME, "Select-control")
            bar_select.click()
            time.sleep(1)

            bar_options = self.driver.find_elements(
                By.CLASS_NAME, "VirtualizedSelectOption"
            )
            assert len(bar_options) > 0, "Bar chart dropdown should have options"

            # Select Normalized option
            for option in bar_options:
                if option.text == "Normalized":
                    option.click()
                    break
            time.sleep(2)

            bar_selected = bar_dropdown.find_element(
                By.CLASS_NAME, "Select-value-label"
            )
            assert bar_selected.text == "Normalized", "Bar chart should show Normalized"

            charts = ["waiting-line-chart", "housing-bar-chart"]
            for chart_id in charts:
                chart = self.wait.until(
                    EC.presence_of_element_located((By.ID, chart_id))
                )
                assert chart.is_displayed(), f"{chart_id} should remain visible"

        except Exception as e:
            pytest.fail(f"Data type dropdowns test failed: {str(e)}")
