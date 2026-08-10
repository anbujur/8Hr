"""
Simple table finder: progressively scrolls to locate the SLA table.
"""
import time
from selenium.webdriver.common.by import By


def find_and_scroll_to_sla_table(driver, wait_timeout=30):
    """
    Progressively scrolls down and finds the first table with SLA-related headers.
    Returns the table element.
    
    Args:
        driver: Selenium WebDriver instance
        wait_timeout: Max seconds to wait
        
    Returns:
        The table element, or None if not found
    """
    print("Starting progressive scroll to find SLA table...")
    max_scrolls = 30
    
    for attempt in range(max_scrolls):
        try:
            tables = driver.find_elements(By.XPATH, "//table")
        except Exception:
            tables = []
        
        print(f"Scroll attempt {attempt+1}/{max_scrolls}, found {len(tables)} table(s)")
        
        for tidx, tbl in enumerate(tables):
            try:
                if not tbl.is_displayed():
                    continue
                
                # Get header texts
                try:
                    header_cells = tbl.find_elements(By.XPATH, ".//thead//tr[1]/*[self::th or self::td]")
                    if not header_cells:
                        header_cells = tbl.find_elements(By.XPATH, ".//tr[1]/*[self::th or self::td]")
                    headers = [(hc.text or hc.get_attribute('textContent') or '').strip() for hc in header_cells]
                except Exception:
                    headers = []
                
                header_text = ' | '.join(headers).lower()
                
                # Look for SLA-related keywords
                if any(k in header_text for k in ['measure date', 'lp 12 hrs', 'lp 8 hrs', 'lp 24 hrs', 'total sat', 'lp total']):
                    print(f"✓ Found SLA table #{tidx} with headers: {header_text[:150]}")
                    
                    # Scroll to the table with offset for fixed headers
                    try:
                        driver.execute_script(
                            "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.pageYOffset - 120);",
                            tbl,
                        )
                        time.sleep(0.8)
                        print("✓ Scrolled to SLA table")
                    except Exception as e:
                        print(f"Scroll to table failed: {e}. Trying fallback...")
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tbl)
                        time.sleep(0.8)
                    
                    return tbl
            
            except Exception as e:
                print(f"Inspecting table #{tidx} failed: {e}")
        
        # Scroll down and try again
        try:
            driver.execute_script("window.scrollBy(0, 600);")
        except Exception:
            pass
        time.sleep(0.6)
    
    print("✗ Progressive scroll exhausted: SLA table not found")
    return None
