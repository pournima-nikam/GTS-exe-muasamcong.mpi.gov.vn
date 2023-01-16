from datetime import datetime
import mysql.connector as mysql
import pymysql.cursors
import time
import sys,os
import Global_var

def db_connection():
    while True:
        try:
            connection = mysql.connect(host = '185.142.34.92', user = "ams", passwd = "TgdRKAGedt%h", db = "tenders_db")
            # connection = pymysql.connect(host = 'localhost', user = "root", passwd = "Gts@1234", db ="my_db", charset='utf8',cursorclass=pymysql.cursors.DictCursor)
            return connection 
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
            time.sleep(10)

def Error_fun(Error,Function_name,Source_name):
    mydb = db_connection()
    mycursor = mydb.cursor()
    sql1 = "INSERT INTO errorlog_tbl(Error_Message,Function_Name,Exe_Name) VALUES('" + str(Error).replace("'","''") + "','" + str(Function_name).replace("'","''")+ "','"+str(Source_name)+"')"
    mycursor.execute(sql1)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return sql1

def check_Duplication(segfield,get_htmlsource):
    while True:
        try:
            mydb = db_connection()
            mycursor = mydb.cursor()
            if segfield[13] != '' and segfield[24] != '' and segfield[7] != '':
                commandText = "SELECT Posting_Id from asia_tenders_tbl where tender_notice_no = '" + str(segfield[13]) + "' and Country = '" + str(segfield[7]) + "' and doc_last= '" + str(segfield[24]) + "'"
            elif segfield[13] != "" and segfield[7] != "":
                commandText = "SELECT Posting_Id from asia_tenders_tbl where tender_notice_no = '" + str(segfield[13]) + "' and Country = '" + str(segfield[7]) + "'"
            elif segfield[19] != "" and segfield[24] != "" and segfield[7] != "":
                commandText = "SELECT Posting_Id from asia_tenders_tbl where short_desc = '" + str(segfield[19]) + "' and doc_last = '" + segfield[24] + "' and Country = '" + segfield[7] + "'"
            else:
                commandText = "SELECT Posting_Id from asia_tenders_tbl where short_desc = '" + str(segfield[19]) + "' and Country = '" + str(segfield[7]) + "'"
            mycursor.execute(commandText)
            results = mycursor.fetchall()
            mydb.close()
            mycursor.close()
            print("Code Reached On check_Duplication")
            if len(results) > 0:
                print('Duplicate Tender')
                Global_var.duplicate += 1
            else:
                create_html_file(segfield,get_htmlsource)
            break
        except Exception as e:
            Function_name: str = sys._getframe().f_code.co_name
            Error: str = str(e)
            Source_name = str(segfield[31])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
            Error_fun(Error,Function_name,Source_name)
            time.sleep(10)

def create_html_file(segfield,get_htmlsource):

    while True:
        try:
            exe_number = str(Global_var.exe_no)
            Current_dateTime = datetime.now().strftime("%Y%m%d%H%M%S%f")
            Fileid = "".join([exe_number , Current_dateTime])
            Path = "Z:" + Fileid + ".html"
            file1 = open(Path , "w" , encoding='utf-8')
            Final_Doc = "<HTML><head><meta content=\"text/html; charset=utf-8\" http-equiv=\"Content-Type\" /><title>Tender Document</title></head><BODY><Blockquote style='border:1px solid; padding:10px;'>"+get_htmlsource+"<td style=\"padding:7px;\">Click Here For Main Source </td><td style=\"padding:7px;\"><a href='"+ segfield[6] +"' target=\"_blank\">Click Here</a></td></Blockquote></BODY></HTML>"
            file1.write(Final_Doc)
            file1.close()
            
            
            insert_in_local(segfield,Fileid)
            break
        except Exception as e:
            Function_name: str = sys._getframe().f_code.co_name
            Error: str = str(e)
            Source_name = str(segfield[31])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
            Error_fun(Error,Function_name,Source_name)
            time.sleep(10)


def insert_in_local(segfield,Fileid):

    while True:
        mydb = db_connection()
        mycursor = mydb.cursor()
        sql = "INSERT INTO asia_tenders_tbl (Tender_ID,EMail,add1,Country,Maj_Org,tender_notice_no,notice_type,Tenders_details,short_desc,est_cost,currency,doc_cost,doc_last,earnest_money,Financier,tender_doc_file,source)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val= (str(Fileid) ,str(segfield[1]) , str(segfield[2]) , str(segfield[7]) , str(segfield[12]) , str(segfield[13]) , str(segfield[14]),
                str(segfield[18]) , str(segfield[19]) , str(segfield[20]) , str(segfield[21]) , str(segfield[22]), str(segfield[24]),str(segfield[26]) ,str(segfield[27]),
                str(segfield[28]) , str(segfield[31]))
        try:
            mycursor.execute(sql , val)
            mydb.commit()
            mydb.close()
            mycursor.close()
            print("Code Reached On insert_in_Local")
            insert_l2l_tbl(segfield, Fileid)
            break
        except Exception as e:
            Function_name: str = sys._getframe().f_code.co_name
            Error: str = str(e)
            Source_name = str(segfield[31])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
            Error_fun(Error,Function_name,Source_name)
            time.sleep(10)
        

def insert_l2l_tbl(segfield, Fileid):
    ncb_icb = str(Global_var.ncb_icb)
    dms_entrynotice_tblstatus = "1"
    added_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    search_id = "1"
    cpv_userid = ""
    dms_entrynotice_tblquality_status = '1'
    quality_id = '1'
    quality_addeddate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Col1 = str(Global_var.Col1)
    if segfield[7] == "IN":
        Col2 = str(segfield[26]) + " * " + str(segfield[20])  # For India Only Other Wise Blank
    else:
        Col2 = ''
    Col3 = ''
    Col4 = ''
    Col5 = ''
    file_name = "D:\\Tide\\DocData\\" + Fileid + ".html"
    file_upload = str(Global_var.file_upload)
    dms_downloadfiles_tbluser_id = str(Global_var.dms_downloadfiles_tbluser_id)
    dms_downloadfiles_tblstatus = '1'
    dms_downloadfiles_tblsave_status = '1'
    selector_id = ''
    select_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dms_downloadfiles_tbldatatype = "A"
    dms_entrynotice_tblnotice_type = '2'
    dms_entrynotice_tbl_cqc_status = '1'
    file_id = Fileid
    is_english = str(Global_var.is_english)
    mydb = db_connection()
    mycursor = mydb.cursor()
    if segfield[12] != "" and segfield[19] != "" and segfield[24] != "" and segfield[7] != "" and segfield[2] != "":
        dms_entrynotice_tblcompulsary_qc = "2"
    else:
        dms_entrynotice_tblcompulsary_qc = "1"
        Global_var.QC_Tenders += 1
        sql = "INSERT INTO qctenders_tbl(Source,tender_notice_no,short_desc,doc_last,Maj_Org,Address,doc_path,Country)VALUES(%s,%s,%s,%s,%s,%s,%s,%s) "
        val = (str(segfield[31]) , str(segfield[13]) , str(segfield[19]) , str(segfield[24]) , str(segfield[12]) ,str(segfield[2]) , "http://tottestupload3.s3.amazonaws.com/" + file_id + ".html" , str(segfield[7]))
        a4 = 0
        while a4 == 0:
            try:
                mydb = db_connection()
                mycursor = mydb.cursor()
                mycursor.execute(sql , val)
                mydb.commit()
                mycursor.close()
                mydb.close()
                a4 = 1
                print("Code Reached On QC Tenders")
            except Exception as e:
                Function_name: str = sys._getframe().f_code.co_name
                Error: str = str(e)
                Source_name = str(segfield[31])
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
                Error_fun(Error,Function_name,Source_name)
                a4 = 0
                time.sleep(10)

    sql = "INSERT INTO l2l_tenders_tbl(notice_no,file_id,purchaser_name,deadline,country,description,purchaser_address,purchaser_email,purchaser_url,purchaser_emd,purchaser_value,financier,deadline_two,tender_details,ncbicb,status,added_on,search_id,cpv_value,cpv_userid,quality_status,quality_id,quality_addeddate,source,tender_doc_file,Col1,Col2,Col3,Col4,Col5,file_name,user_id,status_download_id,save_status,selector_id,select_date,datatype,compulsary_qc,notice_type,cqc_status,DocCost,DocLastDate,is_english,currency,sector,project_location,set_aside,other_details,file_upload)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (str(segfield[13]) , file_id , str(segfield[12]) , str(segfield[24]) , str(segfield[7]) , str(segfield[19]) ,str(segfield[2]) ,str(segfield[1]) , str(segfield[8]) , str(segfield[26]) , str(segfield[20]) , str(segfield[27]) ,str(segfield[24]) , str(segfield[18]) , ncb_icb , dms_entrynotice_tblstatus , str(added_on) , search_id ,str(segfield[36]) ,cpv_userid , dms_entrynotice_tblquality_status , quality_id , str(quality_addeddate) , str(segfield[31]) ,str(segfield[28]) ,Col1 , Col2 , Col3 , Col4 , Col5 ,file_name , dms_downloadfiles_tbluser_id , dms_downloadfiles_tblstatus , dms_downloadfiles_tblsave_status ,selector_id , str(select_date) , dms_downloadfiles_tbldatatype ,dms_entrynotice_tblcompulsary_qc , dms_entrynotice_tblnotice_type , dms_entrynotice_tbl_cqc_status ,str(segfield[22]) , str(segfield[41]),is_english, str(segfield[21]),segfield[29],segfield[42],segfield[43],str(segfield[46]),file_upload)
    a5 = 0
    while a5 == 0:
        try:
            mydb = db_connection()
            mycursor = mydb.cursor()
            mycursor.execute(sql , val)
            mydb.commit()
            mydb.close()
            mycursor.close()
            print("Code Reached On insert_L2L")
            print('😍 Live Tender 😍')
            Global_var.Inserted += 1
            a5 = 1
        except Exception as e:
            Function_name: str = sys._getframe().f_code.co_name
            Error: str = str(e)
            Error_fun(Error,Function_name,segfield)
            Global_var.Print_Exception_detail(e)
            a5 = 0
            time.sleep(10)

db_connection()

