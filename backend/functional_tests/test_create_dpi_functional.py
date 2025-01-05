import unittest
import random
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

# Import for Explicit Wait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException

class TestCreateDPI(StaticLiveServerTestCase):
    """
    End-to-end functional test using Selenium:
      1) Go to landing page.
      2) Click a link/button to navigate to the authentication page.
      3) Log in as 'administratif'.
      4) Redirect to /administratif/creerdpi.
      5) Fill the DPI form and verify success.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()
        # Implicit wait is still okay to keep for short fallback waiting, 
        # but you can remove or adjust as needed
        cls.browser.implicitly_wait(2)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_create_dpi(self):
        wait = WebDriverWait(self.browser, 10)  # WebDriverWait with a 10-second timeout

        # --------------------------------------------------------------------
        # 1. Go to the landing page
        # --------------------------------------------------------------------
        landing_url = "http://localhost:4200/landingpage"
        self.browser.get(landing_url)

        # Wait explicitly until the button/link that takes us to the auth page is clickable
        link_to_auth_locator = (By.XPATH, '//a[span[contains(text(),"Accéder à la plateforme")]]')
        link_to_auth = wait.until(EC.element_to_be_clickable(link_to_auth_locator))
        link_to_auth.click()

        # --------------------------------------------------------------------
        # 2. Log in as 'administratif'
        # --------------------------------------------------------------------
        # Wait for the login form fields to be present on the authentication page
        email_field_locator = (By.ID, "email")
        password_field_locator = (By.ID, "password")
        login_button_locator = (
            By.XPATH,
            '//button[span[contains(text(),"Se Connecter")]]'
        )

        email_field = wait.until(EC.presence_of_element_located(email_field_locator))
        password_field = wait.until(EC.presence_of_element_located(password_field_locator))

        email_field.send_keys("selenium@selenium.com")
        password_field.send_keys("password123")

        login_button = wait.until(EC.element_to_be_clickable(login_button_locator))
        login_button.click()

        # --------------------------------------------------------------------
        # 3. Wait for the redirect to /administratif/creerdpi and form load
        # --------------------------------------------------------------------
        # We’ll wait for the first DPI form field to appear:
        patient_nom_field_locator = (By.CSS_SELECTOR, '[formControlName="patient_nom"]')
        patient_nom_field = wait.until(EC.presence_of_element_located(patient_nom_field_locator))
        
        # Fill the Step 1 of the DPI creation form
        patient_nom_field.send_keys("TestNom")

        prenom_field_locator = (By.CSS_SELECTOR, '[formControlName="prenom"]')
        prenom_field = self.browser.find_element(*prenom_field_locator)
        prenom_field.send_keys("TestPrenom")

        nss_field_locator = (By.CSS_SELECTOR, '[formControlName="nss"]')
        nss_field = self.browser.find_element(*nss_field_locator)
        nss_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        nss_field.send_keys(nss_number)

        date_naissance_field_locator = (By.CSS_SELECTOR, '[formControlName="date_naissance"]')
        date_naissance_field = self.browser.find_element(*date_naissance_field_locator)
        date_naissance_field.send_keys("01-01-1990")
        time.sleep(1)

        # For 'médecin traitant', we open the mat-select and pick the first option
        medecin_select = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="medecin_traitant"]')
        medecin_select.click()
        time.sleep(1)
        first_medecin_option = self.browser.find_element(By.CSS_SELECTOR, 'mat-option')
        first_medecin_option.click()

        # For 'sexe'
        sexe_select_locator = (By.CSS_SELECTOR, '[formControlName="sexe"]')
        sexe_select = self.browser.find_element(*sexe_select_locator)
        sexe_select.click()

        homme_option_locator = (By.XPATH, '//mat-option[contains(.,"Homme")]')
        homme_option = wait.until(EC.element_to_be_clickable(homme_option_locator))
        homme_option.click()

        # Next step
        step1_next_button = self.browser.find_element(By.CSS_SELECTOR, 'button[matStepperNext]:not([disabled])')
        step1_next_button.click()
        time.sleep(1)

        # --------------------------------------------------------------------
        # 4. Fill the Step 2 of the DPI creation form
        # --------------------------------------------------------------------
        telephone_field_locator = (By.CSS_SELECTOR, '[formControlName="telephone"]')
        telephone_field = wait.until(EC.presence_of_element_located(telephone_field_locator))
        telephone_field.send_keys("0540564747")

        personne_contact_field_locator = (By.CSS_SELECTOR, '[formControlName="personne_contact"]')
        personne_contact_field = self.browser.find_element(*personne_contact_field_locator)
        personne_contact_field.send_keys("John Doe")

        adresse_field_locator = (By.CSS_SELECTOR, '[formControlName="adresse"]')
        adresse_field = self.browser.find_element(*adresse_field_locator)
        adresse_field.send_keys("123 Rue Angular")

        mutuelle_field_locator = (By.CSS_SELECTOR, '[formControlName="mutuelle"]')
        mutuelle_field = self.browser.find_element(*mutuelle_field_locator)
        mutuelle_field.send_keys("Test Mutuelle")
        time.sleep(1)

         # Scroll the button into view
        step2_next_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Suivant')]")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", step2_next_button)
        time.sleep(1)

        # Ensure the button is clickable
        self.browser.execute_script("arguments[0].click();", step2_next_button)
        time.sleep(1)

        # --------------------------------------------------------------------
        # 5. Fill the Step 3 of the DPI creation form
        # --------------------------------------------------------------------
        patient_email_field_locator = (By.CSS_SELECTOR, '[formControlName="patient_email"]')
        patient_email_field = wait.until(EC.presence_of_element_located(patient_email_field_locator))
        unique_email = f"testpatient{random.randint(1000, 9999)}@selenium.com"
        patient_email_field.send_keys(unique_email)

        patient_password_field_locator = (By.CSS_SELECTOR, '[formControlName="patient_password"]')
        patient_password_field = self.browser.find_element(*patient_password_field_locator)
        patient_password_field.send_keys("password123")

        confirm_password_field_locator = (By.CSS_SELECTOR, '[formControlName="confirmPassword"]')
        confirm_password_field = self.browser.find_element(*confirm_password_field_locator)
        confirm_password_field.send_keys("password123")

        # Click "Créer dossier"
        create_button_locator = (By.XPATH, '//button[contains(text(),"Créer dossier")]')
        create_button = wait.until(EC.element_to_be_clickable(create_button_locator))
        create_button.click()

        # --------------------------------------------------------------------
        # 6. Verify success message
        # --------------------------------------------------------------------
        # Wait for the success message to appear in the body
        body_locator = (By.TAG_NAME, "body")
        wait.until(EC.text_to_be_present_in_element(body_locator, 
            "Le dossier du patient a été créé avec succès")
        )

        body_text = self.browser.find_element(*body_locator).text
        self.assertIn(
            "Le dossier du patient a été créé avec succès",
            body_text,
            "Success message not found after creating the DPI."
        )

if __name__ == "__main__":
    unittest.main()
