import logging
from rto_processor.processor import RTOProcessor
from rto_processor.browser import Browser
from rto_processor.utils import *
from configs import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize browser and processor
        browser = Browser()
        processor = RTOProcessor(browser)
        
        # Start the scraping process
        start_scrapper(processor)
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        raise
    finally:
        try:
            if 'browser' in locals():
                browser.driver.quit()
                logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error while closing browser: {str(e)}")

def start_scrapper(processor):
    """Main function to start the RTO data scraping process."""
    try:
        log_message("\n=== Starting RTO-wise processing ===")
        year_state_mapping = config.YEAR_STATE_MAPPING
        
        # Track failed processes
        failed_processes = []
        
        for year, states in year_state_mapping.items():
            for state in states:
                log_message(f"\nProcessing state: {state}, Year: {year}")
                
                # Process RTOs for this state and year
                failed_rtos = process_rto_wise_data(processor, state, year)
                
                if failed_rtos:
                    failed_processes.append({
                        'state': state,
                        'year': year,
                        'failed_rtos': failed_rtos
                    })
        
        # Log summary of failed processes
        if failed_processes:
            log_message("\n=== Processing Summary (Failed) ===")
            for process in failed_processes:
                log_message(f"Failed to process {len(process['failed_rtos'])} RTOs in {process['state']} ({process['year']}):")
                for rto in process['failed_rtos']:
                    log_message(f"  - {rto}")
        else:
            log_message("\n=== All RTOs processed successfully ===")
            
    except Exception as e:
        log_message(f"Error in start_scrapper: {str(e)}", exc_info=True)
        raise

def handle_503_and_recover(processor, retry_delay=900):
    """
    Handle recovery from a 503 Bad Gateway error.
    Waits, refreshes the page, and re-sets axis configuration.
    """
    log_message(f"503 error detected. Waiting {retry_delay // 60} minutes before retrying...")
    time.sleep(retry_delay)

    try:
        processor.browser.driver.refresh()
        WebDriverWait(processor.browser.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[name='javax.faces.ViewState']"))
        )
        log_message("Page refreshed. Re-attempting axis setup...")
        
        if not processor.setup_axis():
            raise Exception("Axis setup failed after 503 recovery")
        
        log_message("Axis re-setup successful after 503 recovery.")
        return True
    except Exception as e:
        log_message(f"Failed to recover after 503: {str(e)}")
        return False


def process_rto_wise_data(processor, state_name, year, specific_rtos=None):
    """
    Process RTO-wise data for a given state and year.

    Args:
        processor: RTOProcessor instance
        state_name: Name of the state to process
        year: Year to process data for
        specific_rtos: Optional list of specific RTOs to process (for retries)

    Returns:
        list: List of RTOs that failed to process
    """
    failed_rtos = []

    def handle_503_and_recover():
        log_message("503 error detected. Waiting 15 minutes before retrying...")
        time.sleep(900)
        try:
            processor.browser.driver.refresh()
            WebDriverWait(processor.browser.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[name='javax.faces.ViewState']"))
            )
            return processor.setup_axis()
        except Exception as e:
            log_message(f"Failed to recover from 503: {str(e)}")
            return False

    try:
        log_message(f"\n=== Starting RTO-wise processing for {state_name}, {year} ===")

        # Setup axis configuration
        if processor.check_for_503_error():
            if not handle_503_and_recover():
                return ["All RTOs (503 during setup_axis)"]

        if not processor.setup_axis():
            log_message("Failed to setup axis configuration")
            return ["All RTOs (axis setup failed)"]

        if processor.check_for_503_error():
            if not handle_503_and_recover():
                return ["All RTOs (503 after axis setup)"]

        if not processor.select_state_primefaces(state_name):
            log_message(f"Failed to select state: {state_name}")
            return ["All RTOs (state selection failed)"]

        if processor.check_for_503_error():
            if not handle_503_and_recover():
                return ["All RTOs (503 after state selection)"]

        if not processor.select_year(year):
            log_message(f"Failed to select year: {year}")
            return ["All RTOs (year selection failed)"]

        if processor.check_for_503_error():
            if not handle_503_and_recover():
                return ["All RTOs (503 after year selection)"]

        rto_list = specific_rtos or processor.get_all_rtos_for_state()
        if not rto_list:
            log_message("No RTOs found for the selected state")
            return ["All RTOs (no RTOs found)"]

        for rto in rto_list:
            success = False
            retry_attempts = 2

            for attempt in range(retry_attempts):
                try:
                    log_message(f"\nProcessing RTO: {rto} (Attempt {attempt + 1})")

                    if processor.check_for_503_error():
                        if not handle_503_and_recover():
                            failed_rtos.append(rto)
                            break
                        continue

                    if not processor.select_specific_rto(rto):
                        raise Exception("RTO selection failed")

                    if processor.check_for_503_error():
                        if not handle_503_and_recover():
                            failed_rtos.append(rto)
                            break
                        continue

                    if not processor.apply_filters():
                        raise Exception("Filter application failed")

                    if processor.check_for_503_error():
                        if not handle_503_and_recover():
                            failed_rtos.append(rto)
                            break
                        continue

                    if not processor.download_excel_rto(state_name, year, rto):
                        raise Exception("Download failed")

                    log_message(f"Successfully processed RTO: {rto}")
                    success = True
                    break

                except Exception as e:
                    log_message(f"Error processing RTO {rto}: {str(e)}")
                    if processor.check_for_503_error():
                        if not handle_503_and_recover():
                            break

            if not success:
                failed_rtos.append(rto)

            random_delay(2, 5)  # Delay between RTOs

        return failed_rtos

    except Exception as e:
        log_message(f"Error in process_rto_wise_data: {str(e)}", exc_info=True)
        return ["All RTOs (unexpected error)"]
    
if __name__ == "__main__":
    main()
