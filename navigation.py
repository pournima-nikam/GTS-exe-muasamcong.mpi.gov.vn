from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import Global_var
from datetime import datetime, timedelta
import re
from insert_on_database import *
import wx
app = wx.App()
# from time import sleep
import html

def chromedriver():
    browser = webdriver.Chrome('C:\\Translation EXE\\chromedriver.exe')
    browser.get('https://muasamcong.mpi.gov.vn/en/web/guest/contractor-selection?render=index')
    browser.maximize_window()
    time.sleep(2)
    navigation(browser)

def remove_html(text):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr,'',str(text))
    return cleantext


def navigation(browser):


    # for from_date in browser.find_elements(By.XPATH,'//*[@id="headerSearchTabContent"]/div/div/div/div[2]/div/div[1]/div/div/div/span/span/input[1]'):
    #     browser.execute_script("arguments[0].value = arguments[1]" , from_date , str(Global_var.From_Date))
    #     time.sleep(2)
    #     break
    # for to_date in browser.find_elements(By.XPATH,'//*[@id="headerSearchTabContent"]/div/div/div/div[2]/div/div[1]/div/div/div/span/span/input[2]'):
    #     browser.execute_script("arguments[0].value = arguments[1]" , to_date , str(Global_var.To_Date))
    #     time.sleep(2)
    #     break
    # for button in browser.find_elements(By.XPATH,'//*[@id="headerSearchTabContent"]/div/div/div/div[2]/div/div[2]/div/div/div/button'):

    #     browser.execute_script("arguments[0].click();", button)

    #     # button.click()
    #     time.sleep(5)
        
    
    div_count = 1 # count starts from 1
    collected_list = []
    # page_count = 1
    error = True
    while error == True:
        for _ in browser.find_elements(By.XPATH,'//*[@id="bid-closed"]/div'):
            for link in browser.find_elements(By.XPATH,'//*[@id="bid-closed"]/div['+str(div_count)+']/div/div[2]/div[1]/a'): # div count changes in link
                link_href = link.get_attribute('href')
                print(link_href)
                # collected_list.append(link_href)
                break
            for outerhtml in browser.find_elements(By.XPATH,'//*[@id="bid-closed"]/div['+str(div_count)+']'):
                outerhtml_text = outerhtml.get_attribute('outerHTML')
                
                closing_date = outerhtml_text.partition('Thời điểm đóng thầu</p>')[2].partition('</h5> <p>')[0]
                closing_date_text = remove_html(closing_date).strip()
                format_date = datetime.strptime(closing_date_text, '%H:%M %d/%m/%Y')
                final_date = format_date.strftime('%Y-%m-%d')
                
                publish_date = outerhtml_text.partition('Ngày đăng tải thông báo: <span>')[2].partition('</span>')[0]
                publish_date_text = publish_date.partition('-')[0].strip()
                date = datetime.strptime(publish_date_text, '%d/%m/%Y') 
                selected_date = datetime.strptime(Global_var.From_Date, '%d/%m/%Y') # from date from main calendar
                timedelta = date - selected_date # how many days remaining 
                day = timedelta.days
                if day >= 0:
                    collected_list.append({"link_href": link_href, "closing_date": final_date})
                    div_count += 1
                else:
                    error = False
            
            
            # for publish_date in browser.find_elements(By.XPATH,'//*[@id="other-tbmt"]/div/div[2]/div/div/div[3]/div['+str(div_count)+']/div/div[2]/div/div[1]/div/div[4]/div/div[2]/p'): # publish date path
            #     publish_date_text = publish_date.get_attribute('innerText')
                # date = datetime.strptime(publish_date_text, '%d/%m/%Y %H:%M') 
                # selected_date = datetime.strptime(Global_var.From_Date, '%d/%m/%Y') # from date from main calendar
                # timedelta = date - selected_date # how many days remaining 
                # day = timedelta.days
                # if day >= 0:
                #     collected_list.append(link_href)
                #     div_count += 1
                # else:
                #     error = False
                
        # if page_count != 5:
    
        if error != False:
            while True:
                try:
                    for next_page in browser.find_elements(By.XPATH,'//*[@id="search-home"]/div[3]/div[2]/div/div/button[2]'):
                        # browser.execute_script("arguments[0].scrollIntoView(true);", next_page)
                        next_page_text = next_page.get_attribute("outerHTML")                        
                        if "disabled" not in next_page_text:                    
                            next_page.click()
                            time.sleep(5)
                            div_count = 1
                            error = True
                            # page_count += 1
                        else:
                            error = False
                    break
                except:
                    print('Problem on clicking next page')
                    wx.MessageBox("Please visit on website ",Global_var.source_name ,  wx.OK | wx.ICON_INFORMATION)            
        else:
            error = False            
        # else:
        #     error = False
    scrap(browser, collected_list)

    wx.MessageBox('Total: '+ str(len(collected_list)) +'\nInserted: ' + str(Global_var.Inserted) +'\nExpired: '+ str(Global_var.expired) +'\nDuplicate: ' + str(Global_var.duplicate)+ '\nQC_Tenders: ' +str(Global_var.QC_Tenders) +'\nDeadline_Not_given: ' + str(Global_var.Deadline_Not_given), Global_var.source_name ,  wx.OK | wx.ICON_INFORMATION)
    # wx.MessageBox('Message Box Dialog Warning Icon', 'Dialog', wx.OK | wx.ICON_WARNING)
    # wx.MessageBox('Message Box Dialog Error Icon', 'Dialog', wx.OK | wx.ICON_ERROR)
    browser.quit()
    sys.exit()
    
    
def scrap(browser, collected_list):
    for link in collected_list:
        browser.get(link["link_href"])
        time.sleep(2)
        error_r = True
        while error_r == True: 
            try:
                segfield = []

                for _ in range(50):
                    segfield.append('')
                for data in browser.find_elements(By.XPATH,'//*[@id="tender-notice"]/div[2]'):
                    data_html = data.get_attribute('outerHTML').replace('<!---->',' ')
                    get_htmlsource = re.sub("\s+"," ",data_html)
                    break
                    # print(get_htmlsource)
                
                tender_no = get_htmlsource.partition('Mã TBMT </div>')[2].partition('</div>')[0]
                tender_no_text = remove_html(tender_no).strip()
                segfield[13] = tender_no_text
                # print(tender_no_text)

                bidding_party = get_htmlsource.partition('Bên mời thầu </div>')[2].partition('</div>')[0]
                bidding_party_text = remove_html(bidding_party).strip()
                segfield[12] = bidding_party_text.upper()
                # print(bidding_party_text)

                address = get_htmlsource.partition('Địa điểm thực hiện gói thầu </div>')[2].partition('</div>')[0]
                address_text = remove_html(address).strip()
            
                if address_text != '':
                    segfield[2] = address_text.title()
                    # print(address_text)
                else:
                    segfield[2] = "Viet Nam <br>\n[Disclaimer : For Exact Organization/Tendering Authority details, please refer the tender notice.]"
                
                if len(segfield[2]) >= 150:
                    segfield[2] = str(segfield[2])[:150]+'...'
                
                segfield[18] = ''
                    
                tender_title = get_htmlsource.partition('Tên gói thầu </div>')[2].partition('</div>')[0]
                tender_title_text = remove_html(tender_title).strip()
                segfield[19] = tender_title_text.title()
                # print(tender_title_text)

                bid_security_amount = get_htmlsource.partition('Số tiền đảm bảo dự thầu </div>')[2].partition('</div>')[0]
                bid_security_amount_text = remove_html(bid_security_amount).strip()
                # print(bid_security_amount_text)

                duration = get_htmlsource.partition('Thời gian thực hiện hợp đồng </div>')[2].partition('</div>')[0]
                duration_text = remove_html(duration).strip()
                # print(duration_text)

                selection_method = get_htmlsource.partition('Phương thức lựa chọn nhà thầu </div>')[2].partition('</div>')[0]
                selection_method_text = remove_html(selection_method).strip()
                # print(selection_method_text)

                domestic_international = get_htmlsource.partition('Trong nước/ Quốc tế </div>')[2].partition('</div>')[0]
                domestic_international_text = remove_html(domestic_international).strip()
                # print(domestic_international_text)
                if domestic_international_text == "Trong nước":
                    Global_var.ncb_icb = 'ncb'
                else:
                    Global_var.ncb_icb = 'icb'

                fee = get_htmlsource.partition('Chi phí nộp e-HSDT </div>')[2].partition('</div>')[0]
                fee_text = remove_html(fee).strip().replace(",","" )
                # print(fee_text)

                segfield[46] = 'Phương thức lựa chọn nhà thầu :' + selection_method_text + '<br>\nThời gian thực hiện hợp đồng :' + duration_text + '<br>\nSố tiền đảm bảo dự thầu :' + bid_security_amount_text + '<br>\nChi phí nộp e-HSDT :' + fee_text
                
                opening_date = get_htmlsource.partition('Thời điểm mở thầu </div>')[2].partition('</div>')[0]
                opening_date_text = remove_html(opening_date).strip()
                open = datetime.strptime(opening_date_text,"%d/%m/%Y %H:%M")
                open_date = open.strftime("%Y-%m-%d")
                segfield[25] =  open_date
                # print(opening_date_text)

                segfield[7] = "VN"
                
                segfield[27] = "0"
                
                segfield[28] = str(browser.current_url)
                
                segfield[31] = "muasamcong.mpi.gov.vn"
                
                segfield[42] = segfield[7]
                
                segfield[6] = link["link_href"]

                # closing_date = get_htmlsource.partition('Thời điểm đóng thầu </p>')[2].partition('</p> <button type=')[0]
                # closing_date_text = remove_html(closing_date).strip()
                # format_date = datetime.strptime(closing_date_text, '%d/%m/%Y %H:%M')
                # final_date = format_date.strftime('%Y-%m-%d')
                
                segfield[24] = link["closing_date"] 
                # print(final_date)
                
                for SegIndex, segfield_data in enumerate(segfield):
                    print(SegIndex, segfield_data)
                    segfield[SegIndex] = html.unescape(str(segfield[SegIndex]))
                    segfield[SegIndex] = str(segfield[SegIndex]).replace("'", "''")
            
                if segfield[18] == '':
                    segfield[18] = segfield[19]
                    
                if len(segfield[19]) >= 200:
                    if segfield[18] != segfield[19]:
                        segfield[18] = segfield[19]+'<br>\n'+segfield[18]
                    segfield[19] = str(segfield[19])[:200]+'...'
                    
                if len(segfield[46]) >= 1500:
                    segfield[46] = str(segfield[46])[:1500]+'...'
                
                check_date(segfield,get_htmlsource)
                error_r = False
                # Global_var.Total += 1
                print(" Total: " + str(len(collected_list)) + " Duplicate: " + str(Global_var.duplicate) + " Expired: " + str(Global_var.expired) + " Inserted: " + str(Global_var.Inserted) + " Deadline Not given: " + str(Global_var.Deadline_Not_given) + " QC Tenders: "+ str(Global_var.QC_Tenders),"\n")
            except Exception as e:
                error_r = True
                print(e)   

def check_date(segfield,get_htmlsource):
    
    deadline = (segfield[24])
    curdate = datetime.now()
    curdate_str = curdate.strftime("%Y-%m-%d")
    try:
        if deadline != '':
            datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
            datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
            timedelta_obj = datetime_object_deadline - datetime_object_curdate
            day = timedelta_obj.days
            if day > 0:
                check_Duplication(segfield,get_htmlsource)
            else:
                print("Expired Tender")
                Global_var.expired += 1
        else:
            Global_var.Deadline_Not_given += 1
    except Exception as e:
        print(e)


chromedriver()    