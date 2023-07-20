import requests
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.wait import WebDriverWait


def rundjb(kno):
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	options = Options()
	options.add_argument("--headless=new")
	driver = webdriver.Chrome(options=options)
	driver.implicitly_wait(0.5)
	driver.get("https://djb.gov.in/DJBRMSPortal/portal/payOnline.html")
	time.sleep(5)
	driver.find_element(by=By.XPATH, value="//*[@id='paymenetService']").click()
	time.sleep(5)
	driver.find_element(by=By.XPATH, value="//*[@id='KNO']").send_keys(kno)
	time.sleep(5)
	driver.find_element(by=By.XPATH, value="//*[@id='getBillDetails']").click()
	time.sleep(5)
	final_data = {
		"bill_name": driver.find_element(By.XPATH, "//*[@id='billName']").text,
		"bill_address": driver.find_element(By.XPATH, "//*[@id='billAdr']").text,
		"bill_date": driver.find_element(By.XPATH, "//*[@id='billDate']").text,
		"bill_due": driver.find_element(By.XPATH, "//*[@id='billDue']").text,
		"bill_number": driver.find_element(By.XPATH, "//*[@id='billNum']").text,
		"bill_amount": driver.find_element(By.XPATH, "//*[@id='billAmt']").text
	}
	# close browser
	driver.quit()
	return final_data


def runigl(bp_number):
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	options = Options()
	options.add_argument("--headless=new")
	driver = webdriver.Chrome(options=options)
	driver.implicitly_wait(0.5)
	driver.get(
		"https://webonline.igl.co.in:8077/sap/bc/bsp/sap/zumcui5/webcontent/index.html?directPayment&_ga=2.232730847.1392481746.1673078950-98815281.1673078950#page|%7B%22id%22%3A%22instaPayment%22%7D|id-1673080370177-2|0")
	driver.implicitly_wait(5)
	driver.find_element(by=By.XPATH, value='//*[@id="__field1"]').send_keys(bp_number)
	time.sleep(5)
	driver.find_element(by=By.XPATH, value="//*[@id='__button2']").click()
	time.sleep(5)
	final_data = {
		"first_name": driver.find_element(By.XPATH, "//*[@id='Fntextfield']").get_attribute('value'),
		"last_name": driver.find_element(By.XPATH, "//*[@id='lninput']").get_attribute('value'),
		"ca_number": driver.find_element(By.XPATH, "//*[@id='__field2']").get_attribute('value'),
		"bill_due_before": driver.find_element(By.XPATH, "//*[@id='__field4']").get_attribute('value'),
		"bill_date_is": driver.find_element(By.XPATH, "//*[@id='__field5']").get_attribute('value'),
		"amount_after_due": driver.find_element(By.XPATH, "//*[@id='__field6']").get_attribute('value'),
		"amount_to_paid": driver.find_element(By.XPATH, "//*[@id='finalBA']").get_attribute('value')
	}
	time.sleep(5)
	# close browser
	driver.quit()
	return final_data


def runbses(canumber):
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	options = Options()
	options.add_argument("--headless=new")
	driver = webdriver.Chrome(options=options)
	driver.get(
		f"https://www.bsesdelhi.com/web/brpl/quick-pay-payment?p_p_id=com_bses_pay_now_portlet_BsesPayNowWebPortlet&p_p_lifecycle=0&_com_bses_pay_now_portlet_BsesPayNowWebPortlet_caNo={canumber}".format(
			canumber=canumber))
	driver.implicitly_wait(5)
	time.sleep(5)
	final_data = {
		"ca_number" : canumber,
		"total_demand": driver.find_element(By.XPATH,
											"//*[@id='_com_bses_pay_now_portlet_BsesPayNowWebPortlet_totalDemand']").get_attribute(
			'value'),
		"pending_settlement": driver.find_element(By.XPATH,
												  '//*[@id="_com_bses_pay_now_portlet_BsesPayNowWebPortlet_deferredAmount"]').get_attribute(
			'value'),
		"installment_not_yet_due": driver.find_element(By.XPATH,
													   '//*[@id="_com_bses_pay_now_portlet_BsesPayNowWebPortlet_installmentNotDue"]').get_attribute(
			'value'),
		"round_sum_payable": driver.find_element(By.XPATH,
												 '//*[@id="_com_bses_pay_now_portlet_BsesPayNowWebPortlet_totalDemRoundAmt"]').get_attribute(
			'value'),
		"total_amount": driver.find_element(By.XPATH,
											'//*[@id="_com_bses_pay_now_portlet_BsesPayNowWebPortlet_totalAadvanceAmount"]').get_attribute(
			'value'),
		"due_date": driver.find_element(By.XPATH,
										'//*[@id="_com_bses_pay_now_portlet_BsesPayNowWebPortlet_dueDate"]').get_attribute(
			'value')
	}
	driver.quit()
	return final_data


def runexcitel():
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	options = Options()
	options.add_argument("--headless=new")
	driver = webdriver.Chrome(options=options)
	driver.implicitly_wait(0.5)
	driver.get(
		"https://my.excitel.com/login")
	driver.implicitly_wait(5)
	driver.find_element(by=By.XPATH, value='//*[@id="login"]/div/div[2]/div/form/div[1]/div/input').send_keys(
		"rahul_h124")
	driver.find_element(by=By.XPATH, value='//*[@id="login"]/div/div[2]/div/form/div[2]/div/input').send_keys(
		"11223344")
	time.sleep(5)
	driver.find_element(by=By.XPATH, value='//*[@id="login"]/div/div[2]/div/form/div[3]/div/button').click()
	time.sleep(5)
	WebDriverWait(driver, 10)
	driver.find_element(by=By.XPATH, value='/html/body/app/ng-component/side-nav/nav/div[4]/a').click()
	print("Service Name is : ", driver.find_element(By.XPATH,
													'/html/body/app/ng-component/main/payments/div/div[2]/div[2]/div[2]/div[1]/label[2]').text)
	print("Internet MBPS is : ", driver.find_element(By.XPATH,
													 '/html/body/app/ng-component/main/payments/div/div[2]/div[2]/div[2]/div[2]/label[2]').text)
	print("Service Validity is : ", driver.find_element(By.XPATH,
														'/html/body/app/ng-component/main/payments/div/div[2]/div[2]/div[2]/div[3]/label[2]').text)
	print("Service Expiration Date is : ", driver.find_element(By.XPATH,
															   '/html/body/app/ng-component/main/payments/div/div[2]/div[2]/div[2]/div[5]/label[2]').text)
	print("Plan Amount is : ", driver.find_element(By.XPATH,
												   '/html/body/app/ng-component/main/payments/div/div[2]/div[2]/div[2]/div[6]/label[2]').text)
	print("Payment Amount is : ", driver.find_element(By.XPATH,
													  '/html/body/app/ng-component/main/payments/div/div[2]/div[2]/div[2]/div[7]/label[2]').text)
	print("Extra Charges : ", driver.find_element(By.XPATH,
												  '/html/body/app/ng-component/main/payments/div/div[2]/div[2]/div[2]/div[8]/label[2]').text)
	print("Total Amount is : ", driver.find_element(By.XPATH,
													'/html/body/app/ng-component/main/payments/div/div[2]/div[2]/div[2]/div[9]/label[2]').text)

	driver.quit()


if __name__ == '__main__':
	base_url = "http://172.232.64.45:8000"
	URL = base_url + "/api/method/frappe.tenant_management.doctype.property_overview.property_overview.return_property_list"
	# sending get request and saving the response as response object
	r = requests.get(url=URL)
	# extracting data in json format
	data = r.json()
	if data.get("message"):
		for property in data.get("message"):
			result = {"property": property.get("name"), "djb": {}, "gas": {}, "bses": []}
			if property.get("delhi_jal_board_kno_number"):
				result["djb"] = rundjb(kno=property.get("delhi_jal_board_kno_number"))
			if property.get("gas_bp_number"):
				result["gas"] = runigl(bp_number=property.get("gas_bp_number"))
			for property_bses in property.get("bses_ca_number").split(","):
				if property.get("bses_ca_number"):
					result["bses"].append(runbses(canumber=property_bses.strip()))
			# runexcitel()
			x = requests.post(base_url + "/api/method/frappe.tenant_management.doctype.property_overview.property_overview.create_property_overview", json={"data": result})
			print(x.text)
