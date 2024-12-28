import time
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
import random

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
        # If 'chromedriver' isn't in your PATH, specify its path:
        # cls.browser = webdriver.Chrome(executable_path='/path/to/chromedriver')
        cls.browser = webdriver.Chrome()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_create_dpi(self):
        # --------------------------------------------------------------------
        # 1. Go to the landing page
        # --------------------------------------------------------------------
        landing_url = "http://localhost:4200/landingpage"
        self.browser.get(landing_url)
        time.sleep(2)  # Allow page to load

        # --------------------------------------------------------------------
        # 2. Click the login button/link -> goes to authentication page
        # --------------------------------------------------------------------
        # Example: If there's a button or link with text "Se Connecter":
        #   link_to_auth = self.browser.find_element(By.LINK_TEXT, "Se Connecter")
        # or, if there's an anchor with href="/authentication":
        #   link_to_auth = self.browser.find_element(By.CSS_SELECTOR, 'a[href="/authentication"]')
        #
        # Adjust the selector below to match your real landing page DOM:
        link_to_auth = self.browser.find_element(By.XPATH, '//a[span[contains(text(),"Accéder à la plateforme")]]')
        link_to_auth.click()

        time.sleep(2)  # Wait for nav to authentication page

        # --------------------------------------------------------------------
        # 3. Log in as 'administratif'
        # --------------------------------------------------------------------
        # The route is now http://localhost:4200/authentication (according to your app routes).
        # The form has inputs with id="email" and id="password".
        email_field = self.browser.find_element(By.ID, "email")
        email_field.send_keys("mz_soualahmohammed@esi.dz")

        password_field = self.browser.find_element(By.ID, "password")
        password_field.send_keys("password123")

        login_button = self.browser.find_element(
        By.XPATH,
        '//button[span[contains(text(),"Se Connecter")]]'
)
        login_button.click()


        # The authenticate() function in your code will redirect an administratif user
        # to /administratif/creerdpi. We wait a few seconds for the redirect.
        time.sleep(3)

        # --------------------------------------------------------------------
        # 4. Fill the Step 1 of the DPI creation form
        # --------------------------------------------------------------------
        patient_nom_field = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="patient_nom"]')
        patient_nom_field.send_keys("TestNom")

        prenom_field = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="prenom"]')
        prenom_field.send_keys("TestPrenom")

        nss_field = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="nss"]')
        nss_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        nss_field.send_keys(nss_number)

        date_naissance_field = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="date_naissance"]')
        date_naissance_field.send_keys("01-01-1990")

        # For 'médecin traitant', we open the mat-select and pick the first option
        medecin_select = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="medecin_traitant"]')
        medecin_select.click()
        time.sleep(1)
        first_medecin_option = self.browser.find_element(By.CSS_SELECTOR, 'mat-option')
        first_medecin_option.click()

        # For 'sexe', we open the mat-select and pick "Homme"
        sexe_select = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="sexe"]')
        sexe_select.click()
        time.sleep(1)
        homme_option = self.browser.find_element(By.XPATH, '//mat-option[contains(.,"Homme")]')
        homme_option.click()

        # Next step
        step1_next_button = self.browser.find_element(By.CSS_SELECTOR, 'button[matStepperNext]:not([disabled])')
        step1_next_button.click()
        time.sleep(1)

        # --------------------------------------------------------------------
        # 5. Fill the Step 2 of the DPI creation form
        # --------------------------------------------------------------------
        telephone_field = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="telephone"]')
        telephone_field.send_keys("0540564747")

        personne_contact_field = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="personne_contact"]')
        personne_contact_field.send_keys("John Doe")

        adresse_field = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="adresse"]')
        adresse_field.send_keys("123 Rue Angular")

        mutuelle_field = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="mutuelle"]')
        mutuelle_field.send_keys("Test Mutuelle")

        
        # Scroll the button into view
        step2_next_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Suivant')]")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", step2_next_button)
        time.sleep(1)

        # Ensure the button is clickable
        self.browser.execute_script("arguments[0].click();", step2_next_button)
        time.sleep(1)
        # Click the button
        #step2_next_button.click()
        #time.sleep(1)

        # --------------------------------------------------------------------
        # 6. Fill the Step 3 of the DPI creation form
        # --------------------------------------------------------------------
        patient_email_field = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="patient_email"]')
        unique_email = f"testpatient{random.randint(1000, 9999)}@selenium.com"
        patient_email_field.send_keys(unique_email)

        patient_password_field = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="patient_password"]')
        patient_password_field.send_keys("password123")

        confirm_password_field = self.browser.find_element(By.CSS_SELECTOR, '[formControlName="confirmPassword"]')
        confirm_password_field.send_keys("password123")

        # Click "Créer dossier"
        create_button = self.browser.find_element(By.XPATH, '//button[contains(text(),"Créer dossier")]')
        create_button.click()

        time.sleep(3)

        # --------------------------------------------------------------------
        # 7. Verify success message
        # --------------------------------------------------------------------
        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn(
            "Le dossier du patient a été créé avec succès",
            body_text,
            "Success message not found after creating the DPI."
        )


if __name__ == "__main__":
    unittest.main()
