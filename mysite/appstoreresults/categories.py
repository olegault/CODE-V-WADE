import sqlite3
from google_play_scraper import app
import numpy as np

try:
    sqliteConnection = sqlite3.connect('db-final.db')
    sqliteConnection.row_factory = sqlite3.Row
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    cursor = sqliteConnection.execute("SELECT Name FROM 'App Matrix'")
    res = cursor.fetchall()

    #category 1 - 
    category = ['Ava Fertility', 'ExSeed: Sperm & Fertility App', 'Femometer - Fertility Tracker', 'Fertility Astrology 2', 'Fertility Booster: Diet plans', 'Fertility Friend Ovulation App', 'Fertility', 'Ovulation App & Pre', 'Glow Nurture Pregnancy Tracker', 'Glow: Ovulation & Period App', 'Mira Fertility & Cycle Tracker', 'OvaGraph - Official TCOYF App', 'Ovia Pregnancy & Baby Tracker', 'Ovia: Fertility', 'Cycle', 'Health', 'OvuView: Ovulation & Fertility', 'Ovulation & Period Tracker', 'Ovulation & Periods Tracker', 'Ovulation Calculator & Tracker', 'Ovulation Calculator (OC)', 'Ovulation Calculator Fertility', 'Ovulation Calendar & Fertility', 'Ovulation Tracker & Calculator', 'Ovulation Tracker - Femia', 'Tilly: Fertility & IVF support', 'WOOM - Ovulation & Fertility', 'Evoke Fertility Meditations & femSense fertility', 'Prenatal & Postpartum Workout', 'Prenatal Yoga | Down Dog']

    
    #['280days: Pregnancy Diary', 'Asianparent: Pregnancy & Baby', 'Baby2Body: Pregnancy Wellness', 'Bounty - Pregnancy & Baby App', 'GentleBirth Pregnancy App', 'Healofy - Pregnancy & Parenting', 'HiMommy Pregnancy Tracker App', 'My Pregnancy - Pregnancy Tracker', 'Mylo Pregnancy & Parenting App', 'Pregnancy + | Tracker App', 'Pregnancy After Loss App', 'Pregnancy App & Baby Tracker', 'Pregnancy App + Yoga | keleya', 'Pregnancy Calendar & Tracker', 'Pregnancy Tracker', 'Pregnancy Tracker & Baby App', 'Pregnancy Tracker & Baby Guide', 'Pregnancy Tracker | Preglife', 'Pregnancy and Due Date Tracker', 'Pregnancy tracker week by week', 'WeMoms Pregnancy Baby Tracker', 'amma Pregnancy & Baby Tracker']
    
    #['Period and Ovulation Tracking:', 'Always You: Period Tracker', 'Bedsider Reminders', 'Clover - Safe Period Tracker', 'Clue Period Tracker & Calendar', 'Blood: Period & Cycle Tracker', 'Eve Period Tracker: Love & Sex', 'Grace Health period tracker', 'Luna Period Tracker For Teens', 'MeetYou - Period Tracker', 'My Calendar - Period Tracker', 'Period Calendar Period Tracker', 'Period Calendar Pro', 'Period Diary Ovulation Tracker', 'Period Tracker', 'Period Tracker & Diary', 'Period Tracker & Ovulation App', 'Period Tracker Period Calendar', 'Period and Ovulation Tracker', 'Period tracker: cycle calendar', 'Spot On Period', 'Birth Control', 'Stardust: Period Tracker', 'Wocute - Period Calendar', 'WomanLog Period Calendar']
    
    #['Birth Control and Contraception: Aborto Seguro Ipas Mx', 'Alternatives To Abortion', 'Bible Verses on Abortion', 'Birth Control Pill Reminder', 'Birth Control Shot Reminder', 'Contraception', 'Contraceptive Pill Reminder', 'Contraceptive Ring Reminder +', 'Contraceptive pill reminder', 'Drugs in Pregnancy Lactation', 'Ease: Birth Control Reminder', 'Natural Birth Control', 'Natural Cycles - Birth Control', 'Nurx - Healthcare & Rx at Home', 'Obria Direct', 'One Million Babies - Gravidapp', 'Pearl Fertility', 'Planned Parenthood Direct℠', 'Safe Abort', 'Safe Abortion (SA)', 'Safe abortion with pills', 'The Pill Club: Birth Control', 'WHO Contraception tool', 'iContraception', 'myPill® Birth Control Reminder']

    
    #['Fertility Tracking and Assistance: Ava Fertility', 'ExSeed: Sperm & Fertility App', 'Femometer - Fertility Tracker', 'Fertility Astrology 2', 'Fertility Booster: Diet plans', 'Fertility Friend Ovulation App', 'Fertility', 'Ovulation App & Pre', 'Glow Nurture Pregnancy Tracker', 'Glow: Ovulation & Period App', 'Mira Fertility & Cycle Tracker', 'OvaGraph - Official TCOYF App', 'Ovia Pregnancy & Baby Tracker', 'Ovia: Fertility', 'Cycle', 'Health', 'OvuView: Ovulation & Fertility', 'Ovulation & Period Tracker', 'Ovulation & Periods Tracker', 'Ovulation Calculator & Tracker', 'Ovulation Calculator (OC)', 'Ovulation Calculator Fertility', 'Ovulation Calendar & Fertility', 'Ovulation Tracker & Calculator', 'Ovulation Tracker - Femia', 'Tilly: Fertility & IVF support', 'WOOM - Ovulation & Fertility', 'Evoke Fertility Meditations & femSense fertility', 'Prenatal & Postpartum Workout', 'Prenatal Yoga | Down Dog']



    output = np.array(category)
    i = 0

#add results to table
    for n in output:
        print(output[i])
        cursor.execute('''UPDATE 'App Matrix' SET 'category'=? WHERE Name = ?''', (4, category[i]))
        sqliteConnection.commit()
        i=i+1
    
    cursor.close()

#cannot connect:
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")

import sqlite3
from google_play_scraper import app
import numpy as np

try:
    sqliteConnection = sqlite3.connect('db-final.db')
    sqliteConnection.row_factory = sqlite3.Row
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")


    privpol = 'http://www.smsrobot.com/privacypolicy_period.html'

    analysis = "This is a privacy policy for Lilly Tracker, which is a website and mobile application that provides backup services for storing personal information related to menstruation, fertility, and health. The policy states that the company is committed to protecting and respecting the privacy of its users and will only collect and process personal information in accordance with applicable privacy laws. The policy also includes information about the types of data that may be collected, such as account information, personal data, contact details, technical or other details about the device used to access the Services, and details of the use of the Services. The company states that it will use this data to provide backup services in a reliable and secure manner, present content effectively, provide requested information or services, perform contractual obligations, and notify users about changes to the Services. The policy notes that communications via the Services may reveal certain personal information to other users and that the company is not responsible for the activities of other users or third parties. The policy also explains that the company may store data outside of the European Economic Area (EEA) and that by submitting personal data, users agree to this transfer and processing of data."


    citations = ""


#add results to table
    cursor.execute('''UPDATE 'App Matrix' SET 'chatgpt_analysis'=?, 'chatgpt_citations'=? WHERE privacyPolicy = ?''', (analysis, citations, privpol))
    sqliteConnection.commit()
    cursor.close()

#cannot connect:
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")

