import logging
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
import customtkinter as ctk
from tkinter import messagebox
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configure logging for DEBUG messages
debug_log_filename = 'debug_log.log'
debug_logger = logging.getLogger('debugLogger')
debug_logger.setLevel(logging.DEBUG)  # Set logger level to capture all messages from DEBUG level up.

debug_file_handler = RotatingFileHandler(debug_log_filename, maxBytes=5*1024*1024, backupCount=2)
debug_file_handler.setLevel(logging.DEBUG)  # Set handler level to process all messages it receives from the logger.

debug_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
debug_file_handler.setFormatter(debug_formatter)

debug_logger.addHandler(debug_file_handler)

# Initialize a global list to store item names and prices
item_prices = []

def log_item_prices(driver):
    global item_prices  # Ensure we're modifying the global list
    try:
        # Find all elements that contain item names and prices
        item_elements = driver.find_elements(By.CLASS_NAME, "inventory_item")
        for item_element in item_elements:
            item_name = item_element.find_element(By.CLASS_NAME, "inventory_item_name").text
            item_price = item_element.find_element(By.CLASS_NAME, "inventory_item_price").text
            item_prices.append((item_name, item_price))  # Append each found name and price as a tuple to the global list
            debug_logger.info(f"Item found: {item_name} with price: {item_price}")
    except Exception as e:
        debug_logger.error(f"Failed to log item names and prices: {str(e)}")

def try_add_to_cart(driver, item_xpath, item_name, confirmation_xpath):
    try:
        start_time = time.time()
        add_button = driver.find_element(By.XPATH, item_xpath)
        add_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, confirmation_xpath), "Remove")
        )
        
        elapsed_time = time.time() - start_time
        debug_logger.info(f"Successfully added {item_name} to the cart in {elapsed_time:.2f} seconds")
        return True
    except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
        debug_logger.error(f"Failed to add {item_name} to the cart: {str(e)}")
        return False

def try_remove_from_cart(driver, item_xpath, item_name):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, item_xpath)))
        remove_button = driver.find_element(By.XPATH, item_xpath)
        remove_button.click()
        
        WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.XPATH, item_xpath)))
        
        time.sleep(0.2)  # Visual confirmation
        
        debug_logger.info(f"Successfully removed {item_name} from the cart")
        return True
    except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
        debug_logger.error(f"Failed to remove {item_name} from the cart: {str(e)}")
        return False
        
# Function to run the Selenium test
def run_test(browser):
    succeeded_tests = []
    failed_tests = []
    unexecuted_tests = []
    driver = None
    if browser == "Firefox":
        driver = webdriver.Firefox()
        debug_logger.info("Firefox WebDriver started")
    elif browser == "Edge":
        driver = webdriver.Edge()
        debug_logger.info("Edge WebDriver started")
    else:
        messagebox.showerror("Error", "Browser not supported")
        debug_logger.error("Attempted to start unsupported browser: %s", browser)
        return

    try:
        driver.get("https://www.saucedemo.com/")
        debug_logger.info("Navigated to Sauce Demo")
        time.sleep(2)  # Wait for the page to load

        # Perform login using the selected user
        selected_user = user_var.get()
        driver.find_element(By.ID, "user-name").send_keys(selected_user)
        driver.find_element(By.ID, "password").send_keys("secret_sauce")  # Assuming the password is the same
        driver.find_element(By.ID, "login-button").click()
        debug_logger.info(f"Performed login as {selected_user}")
        succeeded_tests.append("Login")

        time.sleep(2)  # Wait for inventory page to load

        # Check if prices should be logged
        if check_prices_var.get():
            try:
                log_item_prices(driver)
                succeeded_tests.append("Check Prices")  # Add to succeeded tests if prices are checked without errors
            except Exception as e:
                failed_tests.append("Check Prices")  # Add to failed tests if an error occurs during price checking
                debug_logger.error(f"Failed to check item prices: {str(e)}")
        else:
            unexecuted_tests.append("Check Prices")
            debug_logger.info("Check Prices test was not executed")

        # Check and add the backpack if selected
        if backpack_var.get():
            result = try_add_to_cart(driver, "//button[@data-test='add-to-cart-sauce-labs-backpack']", "backpack", "//button[@data-test='remove-sauce-labs-backpack']")
            if result:
                succeeded_tests.append("Add backpack")
            else:
                failed_tests.append("Add backpack")
        else:
            unexecuted_tests.append("Add backpack")
            debug_logger.info("Add backpack test was not executed")

        # Check and add Bike Light if selected
        if bike_light_var.get():
            result = try_add_to_cart(driver, "//button[@data-test='add-to-cart-sauce-labs-bike-light']", "Bike Light", "//button[@data-test='remove-sauce-labs-bike-light']")
            if result:
                succeeded_tests.append("Add Bike Light")
            else:
                failed_tests.append("Add Bike Light")
        else:
            unexecuted_tests.append("Add Bike Light")
            debug_logger.info("Add Bike Light test was not executed")

        # Check and add Bolt T-Shirt if selected
        if bolt_tshirt_var.get():
            result = try_add_to_cart(driver, "//button[@data-test='add-to-cart-sauce-labs-bolt-t-shirt']", "Bolt T-Shirt", "//button[@data-test='remove-sauce-labs-bolt-t-shirt']")
            if result:
                succeeded_tests.append("Add Bolt T-Shirt")
            else:
                failed_tests.append("Add Bolt T-Shirt")
        else:
            unexecuted_tests.append("Add Bolt T-Shirt")
            debug_logger.info("Add Bolt T-Shirt test was not executed")

        # Check and add Fleece Jacket if selected
        if fleece_jacket_var.get():
            result = try_add_to_cart(driver, "//button[@data-test='add-to-cart-sauce-labs-fleece-jacket']", "Fleece Jacket", "//button[@data-test='remove-sauce-labs-fleece-jacket']")
            if result:
                succeeded_tests.append("Add Fleece Jacket")
            else:
                failed_tests.append("Add Fleece Jacket")
        else:
            unexecuted_tests.append("Add Fleece Jacket")
            debug_logger.info("Add Fleece Jacket test was not executed")

        # Check and add Onesie if selected
        if onesie_var.get():
            result = try_add_to_cart(driver, "//button[@data-test='add-to-cart-sauce-labs-onesie']", "Onesie", "//button[@data-test='remove-sauce-labs-onesie']")
            if result:
                succeeded_tests.append("Add Onesie")
            else:
                failed_tests.append("Add Onesie")
        else:
            unexecuted_tests.append("Add Onesie")
            debug_logger.info("Add Onesie test was not executed")

        # Check and add "Test.allTheThings() T-Shirt (Red)" if selected
        if allthethings_tshirt_var.get():
            result = try_add_to_cart(driver, "//button[@data-test='add-to-cart-test.allthethings()-t-shirt-(red)']", "Test.allTheThings() T-Shirt (Red)", "//button[@data-test='remove-test.allthethings()-t-shirt-(red)']")
            if result:
                succeeded_tests.append("Add Test.allTheThings() T-Shirt (Red)")
            else:
                failed_tests.append("Add Test.allTheThings() T-Shirt (Red)")
        else:
            unexecuted_tests.append("Add Test.allTheThings() T-Shirt (Red)")
            debug_logger.info("Add Test.allTheThings() T-Shirt (Red) test was not executed")

        time.sleep(2)  # Wait for the action to complete

        # Check and remove the backpack if selected
        if backpack_remove_var.get():
            result = try_remove_from_cart(driver, "//button[@data-test='remove-sauce-labs-backpack']", "backpack")
            if result:
                succeeded_tests.append("Remove backpack")
            else:
                failed_tests.append("Remove backpack")
        else:
            unexecuted_tests.append("Remove backpack")
            debug_logger.info("Remove backpack test was not executed")

        # Check and remove Bike Light if selected
        if bike_light_remove_var.get():
            result = try_remove_from_cart(driver, "//button[@data-test='remove-sauce-labs-bike-light']", "Bike Light")
            if result:
                succeeded_tests.append("Remove Bike Light")
            else:
                failed_tests.append("Remove Bike Light")
        else:
            unexecuted_tests.append("Remove Bike Light")
            debug_logger.info("Remove Bike Light test was not executed")

        # Check and remove Bolt T-Shirt if selected
        if bolt_tshirt_remove_var.get():
            result = try_remove_from_cart(driver, "//button[@data-test='remove-sauce-labs-bolt-t-shirt']", "Bolt T-Shirt")
            if result:
                succeeded_tests.append("Remove Bolt T-Shirt")
            else:
                failed_tests.append("Remove Bolt T-Shirt")
        else:
            unexecuted_tests.append("Remove Bolt T-Shirt")
            debug_logger.info("Remove Bolt T-Shirt test was not executed")

        # Check and remove Fleece Jacket if selected
        if fleece_jacket_remove_var.get():
            result = try_remove_from_cart(driver, "//button[@data-test='remove-sauce-labs-fleece-jacket']", "Fleece Jacket")
            if result:
                succeeded_tests.append("Remove Fleece Jacket")
            else:
                failed_tests.append("Remove Fleece Jacket")
        else:
            unexecuted_tests.append("Remove Fleece Jacket")
            debug_logger.info("Remove Fleece Jacket test was not executed")

        # Check and remove Onesie if selected
        if onesie_remove_var.get():
            result = try_remove_from_cart(driver, "//button[@data-test='remove-sauce-labs-onesie']", "Onesie")
            if result:
                succeeded_tests.append("Remove Onesie")
            else:
                failed_tests.append("Remove Onesie")
        else:
            unexecuted_tests.append("Remove Onesie")
            debug_logger.info("Remove Onesie test was not executed")

        # Check and remove "Test.allTheThings() T-Shirt (Red)" if selected
        if allthethings_tshirt_remove_var.get():
            result = try_remove_from_cart(driver, "//button[@data-test='remove-test.allthethings()-t-shirt-(red)']", "Test.allTheThings() T-Shirt (Red)")
            if result:
                succeeded_tests.append("Remove Test.allTheThings() T-Shirt (Red)")
            else:
                failed_tests.append("Remove Test.allTheThings() T-Shirt (Red)")
        else:
            unexecuted_tests.append("Remove Test.allTheThings() T-Shirt (Red)")
            debug_logger.info("Remove Test.allTheThings() T-Shirt (Red) test was not executed")

        # Logout test should be the last action
        if logout_test_var.get():
            # Attempt to open the burger menu
            burger_menu_btn_xpath = "//button[@id='react-burger-menu-btn']"
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, burger_menu_btn_xpath))).click()
            time.sleep(1)  # Adjust this sleep time based on the actual behavior of your application
            
            # Check if the burger menu opened successfully by verifying the presence of an element within the menu
            try:
                logout_button_xpath = "//a[@id='logout_sidebar_link']"
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, logout_button_xpath)))
                debug_logger.info("Burger menu opened successfully")
                succeeded_tests.append("Open Burger Menu")
                
                # Proceed with logout
                driver.find_element(By.XPATH, logout_button_xpath).click()
                logout_confirmation_element_xpath = "//input[@id='user-name']"
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, logout_confirmation_element_xpath))
                )
                debug_logger.info("Logout successful")
                time.sleep(3)  # Adjust this sleep time as needed
                succeeded_tests.append("Logout")
            except TimeoutException:
                debug_logger.error("Failed to open burger menu or logout")
                failed_tests.append("Open Burger Menu")
                failed_tests.append("Logout")
        else:
            unexecuted_tests.append("Logout")
            debug_logger.info("Logout test was not executed")

    except Exception as e:
        debug_logger.exception("An error occurred during the test execution: %s", e)
    finally:
        if driver:
            driver.quit()
            debug_logger.info("WebDriver closed")

    # Generate summary in copypasta format
    summary_lines = [
        "🔥🔥🔥 Test Summary 🔥🔥🔥",
        f"👤 Selected User: {selected_user}",  # Include the selected user
        "",
        "✅ Succeeded Tests:",
        "-------------------"
    ]
    summary_lines.extend([f"✔️ {test}" for test in succeeded_tests] if succeeded_tests else ["None 😢"])

    # Only include prices if "Check Prices" test was executed and succeeded
    if "Check Prices" in succeeded_tests:
        summary_lines.extend([
            "",
            "💰 Prices:",
            "----------"
        ])
        if item_prices:
            for name, price in item_prices:
                summary_lines.append(f"💲 {name}: {price}")
        else:
            summary_lines.append("No prices logged 🚫")

    summary_lines.extend([
        "",
        "❌ Failed Tests:",
        "----------------"
    ])
    summary_lines.extend([f"❌ {test}" for test in failed_tests] if failed_tests else ["None 🎉"])

    summary_lines.extend([
        "",
        "⏭️ Unexecuted Tests:",
        "---------------------"
    ])
    summary_lines.extend([f"⏭️ {test}" for test in unexecuted_tests] if unexecuted_tests else ["None 🚫"])

    summary_lines.append("")
    summary_lines.append("Stejně si myslim, že Lapšanský by neměl šéfovat týmu automatického testingu, protože je to kokot. 🍆")

    summary = "\n".join(summary_lines)

    # Write summary to a file with UTF-8 encoding to support emojis and other Unicode characters
    with open("test_summary.txt", "w", encoding="utf-8") as summary_file:
        summary_file.write(summary)

    # Optionally, log the summary as well
    debug_logger.info(summary)

    if failed_tests:
        error_message = "Test finished with problems found: the following items were not successfully processed - " + ", ".join(failed_tests)
        messagebox.showerror("Test Finished with Problems", error_message)
        debug_logger.error(error_message)
    elif unexecuted_tests:
        info_message = "Some tests were not executed: " + ", ".join(unexecuted_tests)
        messagebox.showinfo("Test Information", info_message)
        debug_logger.info(info_message)
    else:
        messagebox.showinfo("Success", "Test completed successfully without any errors.")

# Function to start the test from the UI
def start_test():
    browser = browser_var.get()
    if not browser:
        messagebox.showerror("Error", "Please select a browser")
        debug_logger.error("No browser selected")
        return
    run_test(browser)

# Setting up the customtkinter UI
ctk.set_appearance_mode("System")  # Set theme to match the system
ctk.set_default_color_theme("blue")  # Set color theme

app = ctk.CTk()  # Create the main window
app.title("Martínkův tool na automatické testování")
app.geometry("800x600")  # Adjusted size to fit more checkboxes and layout

# Top section for browser and user selection
top_frame = ctk.CTkFrame(app)
top_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Left section for cart adding/removing
cart_frame = ctk.CTkFrame(app)
cart_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Right section for future functionalities ("2nd section")
second_section_frame = ctk.CTkFrame(app)
second_section_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# 3rd section for price checking
prices_section_frame = ctk.CTkFrame(app)
prices_section_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

# Configure the grid to allow the left, right, and prices sections to expand and fill space
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)
app.grid_rowconfigure(1, weight=1)

# Create a frame specifically for the start_test_button to control its placement and size
button_frame = ctk.CTkFrame(app)
button_frame.grid(row=2, column=0, columnspan=3, pady=20)
button_frame.grid_columnconfigure(0, weight=1)  # Make the frame expand to fill the grid cell

# Place the start_test_button inside this new frame, centered
start_test_button = ctk.CTkButton(button_frame, text="Start Test", command=start_test)
start_test_button.pack()

# Browser selection in top_frame
browser_var = ctk.StringVar()
browser_label = ctk.CTkLabel(top_frame, text="Select Browser:")
browser_label.grid(row=0, column=0, pady=(0, 10))

firefox_radio = ctk.CTkRadioButton(top_frame, text="Firefox", variable=browser_var, value="Firefox")
firefox_radio.grid(row=0, column=1, sticky="w")

edge_radio = ctk.CTkRadioButton(top_frame, text="Edge", variable=browser_var, value="Edge")
edge_radio.grid(row=0, column=2, sticky="w")

# User selection in top_frame
user_label = ctk.CTkLabel(top_frame, text="Select User:")
user_label.grid(row=1, column=0, pady=(10, 2), sticky="w")

user_options = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]

user_var = ctk.StringVar()
user_var.set(user_options[0])  # default value

user_dropdown = ctk.CTkComboBox(top_frame, values=user_options, variable=user_var)
user_dropdown.grid(row=1, column=1, columnspan=2, pady=(0, 10), sticky="ew")

# Define the select_all_items function before referencing it
def select_all_items():
    is_selected = select_all_var.get()
    backpack_var.set(is_selected)
    bike_light_var.set(is_selected)
    bolt_tshirt_var.set(is_selected)
    fleece_jacket_var.set(is_selected)
    onesie_var.set(is_selected)
    allthethings_tshirt_var.set(is_selected)

# Adding a label for the "1st Section: Add to Cart" for clarity
cart_add_label = ctk.CTkLabel(cart_frame, text="1st Section: Add to Cart")
cart_add_label.pack(pady=(0, 10))

# Now, it's safe to create the checkbox that uses select_all_items in cart_frame
select_all_var = ctk.BooleanVar()
select_all_checkbox = ctk.CTkCheckBox(cart_frame, text="Select All", variable=select_all_var, command=select_all_items)
select_all_checkbox.pack(anchor="w")

backpack_var = ctk.BooleanVar()
ctk.CTkCheckBox(cart_frame, text="Add Backpack", variable=backpack_var).pack(anchor="w")

bike_light_var = ctk.BooleanVar()
ctk.CTkCheckBox(cart_frame, text="Add Bike Light", variable=bike_light_var).pack(anchor="w")

bolt_tshirt_var = ctk.BooleanVar()
ctk.CTkCheckBox(cart_frame, text="Add Bolt T-Shirt", variable=bolt_tshirt_var).pack(anchor="w")

fleece_jacket_var = ctk.BooleanVar()
ctk.CTkCheckBox(cart_frame, text="Add Fleece Jacket", variable=fleece_jacket_var).pack(anchor="w")

onesie_var = ctk.BooleanVar()
ctk.CTkCheckBox(cart_frame, text="Add Onesie", variable=onesie_var).pack(anchor="w")

allthethings_tshirt_var = ctk.BooleanVar()
ctk.CTkCheckBox(cart_frame, text="Add Test.allTheThings() T-Shirt (Red)", variable=allthethings_tshirt_var).pack(anchor="w")

cart_remove_label = ctk.CTkLabel(second_section_frame, text="2nd Section: Remove from Cart")
cart_remove_label.pack(pady=(0, 10))

# Define the select_all_items_remove function for the 2nd section
def select_all_items_remove():
    is_selected = select_all_remove_var.get()
    backpack_remove_var.set(is_selected)
    bike_light_remove_var.set(is_selected)
    bolt_tshirt_remove_var.set(is_selected)
    fleece_jacket_remove_var.set(is_selected)
    onesie_remove_var.set(is_selected)
    allthethings_tshirt_remove_var.set(is_selected)

# Adding a "Select All" Checkbox to the 2nd Section
select_all_remove_var = ctk.BooleanVar()
select_all_remove_checkbox = ctk.CTkCheckBox(second_section_frame, text="Select All", variable=select_all_remove_var, command=select_all_items_remove)
select_all_remove_checkbox.pack(anchor="w")

# Adding checkboxes for removing items from the cart in the "2nd section"
backpack_remove_var = ctk.BooleanVar()
ctk.CTkCheckBox(second_section_frame, text="Remove Backpack", variable=backpack_remove_var).pack(anchor="w")

bike_light_remove_var = ctk.BooleanVar()
ctk.CTkCheckBox(second_section_frame, text="Remove Bike Light", variable=bike_light_remove_var).pack(anchor="w")

bolt_tshirt_remove_var = ctk.BooleanVar()
ctk.CTkCheckBox(second_section_frame, text="Remove Bolt T-Shirt", variable=bolt_tshirt_remove_var).pack(anchor="w")

fleece_jacket_remove_var = ctk.BooleanVar()
ctk.CTkCheckBox(second_section_frame, text="Remove Fleece Jacket", variable=fleece_jacket_remove_var).pack(anchor="w")

onesie_remove_var = ctk.BooleanVar()
ctk.CTkCheckBox(second_section_frame, text="Remove Onesie", variable=onesie_remove_var).pack(anchor="w")

allthethings_tshirt_remove_var = ctk.BooleanVar()
ctk.CTkCheckBox(second_section_frame, text="Remove Test.allTheThings() T-Shirt (Red)", variable=allthethings_tshirt_remove_var).pack(anchor="w")

# Move the Logout Test checkbox setup here, under the item removal checkboxes
logout_test_var = ctk.BooleanVar()
logout_test_checkbox = ctk.CTkCheckBox(second_section_frame, text="Logout Test", variable=logout_test_var)
logout_test_checkbox.pack(pady=10)

# 3rd Section: Check Prices
check_prices_var = ctk.BooleanVar()
prices_section_label = ctk.CTkLabel(prices_section_frame, text="3rd Section: Check Prices")
prices_section_label.pack(pady=(0, 10))

check_prices_checkbox = ctk.CTkCheckBox(prices_section_frame, text="Check Prices", variable=check_prices_var)
check_prices_checkbox.pack(anchor="w")

app.mainloop()