@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_messages(event):
    input_text = event.message.text

    if input_text == '@time':
        IST = pytz.timezone('Europe/London')
        datetime_ist = datetime.now(IST)
        HKT = pytz.timezone('Asia/Hong_Kong')
        datetime_hkt = datetime.now(HKT)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=
                            emoji.emojize(':earth_asia:', use_aliases=True) + ' ' +
                            flag.flagize("Current time in :TW:") + ' ' + ':\n\n' +
                            datetime_hkt.strftime('%Y-%m-%d %H:%M:%S') + '\n\n' +
                            emoji.emojize(':earth_africa:', use_aliases=True) + ' ' +
                            flag.flagize("Current time in :GB:") + ' ' + ':\n\n' +
                            datetime_ist.strftime('%Y-%m-%d %H:%M:%S')
                            )
                                )

    # Function that gives the current weather of 2 different
    elif input_text == '@weather':
        owm = OWM('YOUR_TOKEN')
        mgr = owm.weather_manager()

        # UK
        # Get temperature of London
        uk_obs = mgr.weather_at_place('London,GB')
        uk_w = uk_obs.weather
        temp_uk = uk_w.temperature('celsius')
        for e in ['temp_kf', 'temp_max', 'temp_min']:
            temp_uk.pop(e)
        temp_uk2 = str(temp_uk)

        rep = {"{": "", "}": "", "'": "", ", ": " \n", "temp": "溫度", "feels_like": "體感"}

        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        temp_uk2 = pattern.sub(lambda m: rep[re.escape(m.group(0))], temp_uk2)

        # Get detailed status of London
        status_uk = uk_w.detailed_status
        status_replace = {"light rain": emoji.emojize(':umbrella:', use_aliases=True) + "小雨",
                          "rain": emoji.emojize(':umbrella:', use_aliases=True) + "驟雨",
                          "mist": emoji.emojize(':foggy:', use_aliases=True) + "霧",
                          "clouds": emoji.emojize(':cloud:', use_aliases=True) + "有雲",
                          "few clouds": emoji.emojize(':cloud:', use_aliases=True) + "少雲",
                          "broken clouds": emoji.emojize(':cloud:', use_aliases=True) + "碎雲",
                          "scattered clouds": emoji.emojize(':cloud:', use_aliases=True) + "散雲",
                          "overcast clouds": emoji.emojize(':cloud:', use_aliases=True) + "陰雲",
                          "clear sky": emoji.emojize(':milky_way:', use_aliases=True) + "天清"}
        status_replace = dict((re.escape(k), v) for k, v in status_replace.items())
        status_pattern = re.compile("|".join(status_replace.keys()))
        status_uk = status_pattern.sub(lambda m: status_replace[re.escape(m.group(0))], status_uk)

        # Hong Kong
        # Get temperature
        hk_obs = mgr.weather_at_place('Hong Kong, HK')
        hk_w = hk_obs.weather
        temp_hk = hk_w.temperature('celsius')
        for e in ['temp_kf', 'temp_max', 'temp_min']:
            temp_hk.pop(e)
        temp_hk2 = str(temp_hk)

        temp_hk2 = pattern.sub(lambda m: rep[re.escape(m.group(0))], temp_hk2)

        # Get detailed status of HK
        status_hk = hk_w.detailed_status
        status_hk = status_pattern.sub(lambda m: status_replace[re.escape(m.group(0))], status_hk)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=flag.flagize(":GB:即時倫敦天氣 :\n") + temp_uk2 + '\n' + status_uk + '\n\n' +
                                 flag.flagize(":HK:即時香港天氣 :\n") + temp_tw2 + '\n' + status_tw)

        )

    elif input_text == '@countdown':
        def dateDiffInSeconds(date1, date2):
            timedelta = date2 - date1
            return timedelta.days * 24 * 3600 + timedelta.seconds

        def daysHoursMinutesSecondsFromSeconds(seconds):
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            return (days, hours, minutes, seconds)

        end_date = datetime.strptime('2021-12-24 17:00:00', '%Y-%m-%d %H:%M:%S')
        now = datetime.now()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=emoji.emojize(':calendar:') + ' ' + '距離 Christmas' +
                                 emoji.emojize('::christmas_tree::', use_aliases=True) + ' - \n' +
                                 "%d 天, %d 小時 %d 分鐘 %d 秒" % daysHoursMinutesSecondsFromSeconds(
                dateDiffInSeconds(now, end_date)) + ' ' + emoji.emojize(':santa:', use_aliases=True)
                            )
        )
 

   
    elif input_text == '@sonnet':
        sonnet_list = []
        for root, dirs, files in os.walk('My sonnet output/discord'):
            for file in files:
                if file.endswith('.txt'):
                    with open(os.path.join(root, file), 'r') as f:
                        text2 = f.read()
                        sonnet_list.append(text2)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(sonnet_list),
                            sender=Sender(
                                name='AI Shakespeare',
                                # name=None
                                icon_url='https://media.newyorker.com/photos/5a57ced6f686540bff451ef2/1:1/w_1200,h_1200,c_limit/180122_r31326.jpg')
                            ))

# Function that gives current F1 team standing
    elif input_text == '@f1team':
        page_team = requests.get('https://www.formula1.com/en/results.html/2022/team.html')
        tree_team = html.fromstring(page_team.content)
        team_sd = tree_team.xpath('//tr')
        column_headers = []

        for column in team_sd[0]:
            name = column.text_content()
            column_headers.append((name, []))

        for row in range(1, len(team_sd)):
            table_tr = team_sd[row]

            column_count = 0

            for column in table_tr.iterchildren():
                data = column.text_content()
                column_headers[column_count][1].append(data)
                column_count += 1

        dictionary = {title: column for (title, column) in column_headers}

        team_standing = pd.DataFrame(dictionary)

        # data cleaning
        team_standing = team_standing.drop('', 1)
        team_standing['Team'] = team_standing['Team'].str.strip()

        team_pos_list = team_standing['Pos'].tolist()
        team_name_list = team_standing['Team'].tolist()
        team_pts_list = team_standing['PTS'].tolist()

        teamstr = ''
        for i in range(len(team_pos_list)):
            teamstr += team_pos_list[i] + '. ' + team_name_list[i] + ' - ' + team_pts_list[i] + ' PTS\n'
        teamstr = 'Current Constructor Standings: \n\n' + teamstr
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=teamstr,
                            sender=Sender(
                                name='F1',
                                # name=None
                                icon_url='https://cdn.discordapp.com/attachments/813130040938201131/852629478923960350/dux4xq5v0zs41.png')

                            )
                                )


# Fuction that gives the current f1 driver standings
    elif input_text == '@f1driver':
        page_dr = requests.get('https://www.formula1.com/en/results.html/2022/drivers.html')
        tree_dr = html.fromstring(page_dr.content)
        driver_sd = tree_dr.xpath('//tr')
        column_headers = []

        for column in driver_sd[0]:
            name = column.text_content()
            column_headers.append((name, []))

        for row in range(1, len(driver_sd)):
            table_tr = driver_sd[row]

            column_count = 0

            for column in table_tr.iterchildren():
                data = column.text_content()
                column_headers[column_count][1].append(data)
                column_count += 1

        dictionary = {title: column for (title, column) in column_headers}

        driver_standing = pd.DataFrame(dictionary)
        driver_standing = driver_standing.drop('', 1)
        driver_standing['Car'] = driver_standing['Car'].str.strip()
        driver_standing['Driver'] = driver_standing['Driver'].str.strip()
        driver_standing['Driver'] = driver_standing['Driver'].str.replace(" ", "")
        driver_standing['Driver'] = driver_standing['Driver'].str.replace("\n", " ")
        driver_standing['Driver'] = driver_standing['Driver'].str.replace("  ", " ")
        driver_standing['Driver'] = driver_standing['Driver'].str.replace("  ", " ")
        # driver_standing = driver_standing.replace({'Driver': {" ": "", '\n': " "}})

        driver_standing[['First', 'Last', 'Int']] = driver_standing.Driver.str.split(" ", expand=True, )
        driver_standing['Driver'] = driver_standing['First'] + " " + driver_standing['Last']
        driver_standing = driver_standing.drop(['First', 'Last'], axis=1)

        dr_pos_list = driver_standing['Pos'].tolist()
        dr_name_list = driver_standing['Driver'].tolist()
        dr_pts_list = driver_standing['PTS'].tolist()
        dr_str = ''
        for i in range(len(dr_pos_list)):
            dr_str += dr_pos_list[i] + '. ' + dr_name_list[i] + '  -  ' + dr_pts_list[i] + ' PTS\n'

        dr_str = 'Current F1 Driver Standings: \n\n' + dr_str
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=dr_str,
                            sender=Sender(
                                name='F1',
                                # name=None
                                icon_url='https://cdn.discordapp.com/attachments/813130040938201131/852629478923960350/dux4xq5v0zs41.png')

                        )
        )


# Fuction that gives the F1 race time
    elif input_text == '@f1time':
        GP_name = 'Monza GP'
        time_diff = -1
        page_timeTable = requests.get('https://www.formula1.com/en/racing/2021/Italy.html')
        tree_timeTable = html.fromstring(page_timeTable.content)

    #################
        """scrape_list = ['"row js-practice-1"', '"row js-practice-2"',
                       '"row js-practice-3"', '"row js-qualifying"', '"row js-race"']"""

        scrape_list = ['"row js-practice-1"', '"row js-qualifying"',
                       '"row js-practice-2"', '"row js-sprint"', '"row js-race"']

        startTime_list_all = []
        for i in range(len(scrape_list)):
            startTime_list = tree_timeTable.xpath('//div[@class=' + str(scrape_list[i]) + ']/@data-start-time')
            startTime_list_all += startTime_list

        startTime_list_all = [w.replace('T', " ") for w in startTime_list_all]
        startTime_list_all = [datetime.fromisoformat(w) + timedelta(hours=time_diff) for w in startTime_list_all]
        startTime_list_all = [w.strftime("%Y-%m-%d %H:%M:%S") for w in startTime_list_all]

        endTime_list_all = []
        for i in range(len(scrape_list)):
            endTime_list = tree_timeTable.xpath('//div[@class=' + str(scrape_list[i]) + ']/@data-end-time')
            endTime_list_all += endTime_list

        endTime_list_all = [w.replace('T', " ") for w in endTime_list_all]
        endTime_list_all = [datetime.fromisoformat(w) + timedelta(hours=time_diff) for w in endTime_list_all]
        endTime_list_all = [w.strftime("%Y-%m-%d %H:%M:%S") for w in endTime_list_all]

        # startTime_header = ['FP1 Start ', 'FP2 Start ', 'FP3 Start ', 'Quali Start ', 'Race Start ']
        startTime_header = ['FP1 Start ', 'Quali Start ', 'FP2 Start ', 'Sprint Start ', 'Race Start ']

        data_startTime = []
        for (item1, item2) in zip(startTime_header, startTime_list_all):
            data_startTime.append(item1 + item2)

        # endTime_header = ['FP1 End ', 'FP2 End ', 'FP3 End ', 'Quali End ', 'Race End ']
        endTime_header = ['FP1 End ', 'Quali End ', 'FP2 End ', 'Sprint End ', 'Race End ']

        data_endTime = []
        for (item1, item2) in zip(endTime_header, endTime_list_all):
            data_endTime.append(item1 + item2)

        data = []
        for (item1, item2) in zip(data_startTime, data_endTime):
            data.append(item1 + '\n' + item2 + '\n\n')

        outputstr = ''
        for i in range(len(data)):
            outputstr += data[i]

        outputstr = GP_name + ' Time Table\n' + outputstr
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=outputstr,
                            sender=Sender(
                                name='F1',
                                # name=None
                                icon_url='https://cdn.discordapp.com/attachments/813130040938201131/852629478923960350/dux4xq5v0zs41.png')

                        )
        )


# Fuction that gives the F1 race time
    elif input_text == '@f1':
        GP_name = 'Monza GP'
        time_diff = -1
        page_timeTable = requests.get('https://www.formula1.com/en/racing/2021/Italy.html')
        tree_timeTable = html.fromstring(page_timeTable.content)

        #######
        """scrape_list = ['"row js-practice-1"', '"row js-practice-2"',
                       '"row js-practice-3"', '"row js-qualifying"', '"row js-race"']"""

        scrape_list = ['"row js-practice-1"', '"row js-qualifying"',
                       '"row js-practice-2"', '"row js-sprint"', '"row js-race"']

        startTime_list_all = []
        for i in range(len(scrape_list)):
            startTime_list = tree_timeTable.xpath('//div[@class=' + str(scrape_list[i]) + ']/@data-start-time')
            startTime_list_all += startTime_list

        startTime_list_all = [w.replace('T', " ") for w in startTime_list_all]
        startTime_list_all = [datetime.fromisoformat(w) + timedelta(hours=time_diff) for w in startTime_list_all]
        startTime_list_all = [w.strftime("%Y-%m-%d %H:%M:%S") for w in startTime_list_all]

        endTime_list_all = []
        for i in range(len(scrape_list)):
            endTime_list = tree_timeTable.xpath('//div[@class=' + str(scrape_list[i]) + ']/@data-end-time')
            endTime_list_all += endTime_list

        endTime_list_all = [w.replace('T', " ") for w in endTime_list_all]
        endTime_list_all = [datetime.fromisoformat(w) + timedelta(hours=time_diff) for w in endTime_list_all]
        endTime_list_all = [w.strftime("%Y-%m-%d %H:%M:%S") for w in endTime_list_all]

        # startTime_header = ['FP1 Start ', 'FP2 Start ', 'FP3 Start ', 'Quali Start ', 'Race Start ']
        startTime_header = ['FP1 Start ', 'Quali Start ', 'FP2 Start ', 'Sprint Start ', 'Race Start ']

        data_startTime = []
        for (item1, item2) in zip(startTime_header, startTime_list_all):
            data_startTime.append(item1 + item2)

        # endTime_header = ['FP1 End ', 'FP2 End ', 'FP3 End ', 'Quali End ', 'Race End ']
        endTime_header = ['FP1 End ', 'Quali End ', 'FP2 End ', 'Sprint End ', 'Race End ']

        data_endTime = []
        for (item1, item2) in zip(endTime_header, endTime_list_all):
            data_endTime.append(item1 + item2)

        data = []
        for (item1, item2) in zip(data_startTime, data_endTime):
            data.append(item1 + '\n' + item2)

        # New stuff
        fp1start = tree_timeTable.xpath('//div[@class="row js-practice-1"]/@data-start-time')
        fp1start = datetime.fromisoformat(str(fp1start).replace("['", "").replace("']", "")) + timedelta(
            hours=time_diff)
        fp1end = tree_timeTable.xpath('//div[@class="row js-practice-1"]/@data-end-time')
        fp1end = datetime.fromisoformat(str(fp1end).replace("['", "").replace("']", "")) + timedelta(hours=time_diff)

        fp2start = tree_timeTable.xpath('//div[@class="row js-practice-2"]/@data-start-time')
        fp2end = tree_timeTable.xpath('//div[@class="row js-practice-2"]/@data-end-time')
        fp2start = datetime.fromisoformat(str(fp2start).replace("['", "").replace("']", "")) + timedelta(
            hours=time_diff)
        fp2end = datetime.fromisoformat(str(fp2end).replace("['", "").replace("']", "")) + timedelta(hours=time_diff)

        # fp3start = tree_timeTable.xpath('//div[@class="row js-practice-3"]/@data-start-time')
        # fp3end = tree_timeTable.xpath('//div[@class="row js-practice-3"]/@data-end-time')
        # fp3start = datetime.fromisoformat(str(fp3start).replace("['", "").replace("']", "")) + timedelta(hours=time_diff)
        # fp3end = datetime.fromisoformat(str(fp3end).replace("['", "").replace("']", "")) + timedelta(hours=time_diff)

        sprintstart = tree_timeTable.xpath('//div[@class="row js-sprint"]/@data-start-time')
        sprintend = tree_timeTable.xpath('//div[@class="row js-sprint"]/@data-end-time')
        sprintstart = datetime.fromisoformat(str(sprintstart).replace("['", "").replace("']", "")) + timedelta(
            hours=time_diff)
        sprintend = datetime.fromisoformat(str(sprintend).replace("['", "").replace("']", "")) + timedelta(
            hours=time_diff)

        qualistart = tree_timeTable.xpath('//div[@class="row js-qualifying"]/@data-start-time')
        qualiend = tree_timeTable.xpath('//div[@class="row js-qualifying"]/@data-end-time')
        qualistart = datetime.fromisoformat(str(qualistart).replace("['", "").replace("']", "")) + timedelta(
            hours=time_diff)
        qualiend = datetime.fromisoformat(str(qualiend).replace("['", "").replace("']", "")) + timedelta(
            hours=time_diff)

        racestart = tree_timeTable.xpath('//div[@class="row js-race"]/@data-start-time')
        raceend = tree_timeTable.xpath('//div[@class="row js-race"]/@data-end-time')
        racestart = datetime.fromisoformat(str(racestart).replace("['", "").replace("']", "")) + timedelta(
            hours=time_diff)
        raceend = datetime.fromisoformat(str(raceend).replace("['", "").replace("']", "")) + timedelta(hours=time_diff)

        """def getTime():
            if datetime.now() < fp1end:
                test_str = data[0]
            elif datetime.now() < fp2end:
                test_str = data[1]
            elif datetime.now() < fp3end:
                test_str = data[2]
            elif datetime.now() < qualiend:
                test_str = data[3]
            elif datetime.now() < raceend:
                test_str = data[4]
            return test_str"""

        def getTime():
            if datetime.now() < fp1end:
                test_str = data[0]
            elif datetime.now() < qualiend:
                test_str = data[1]
            elif datetime.now() < fp2end:
                test_str = data[2]
            elif datetime.now() < sprintend:
                test_str = data[3]
            elif datetime.now() < raceend:
                test_str = data[4]
            return test_str

        """def getHeader():
            if datetime.now() < fp1start:
                header = 'COMING UP NEXT :\n'
            elif datetime.now() < fp2start:
                header = 'COMING UP NEXT :\n'
            elif datetime.now() < fp3start:
                header = 'COMING UP NEXT :\n'
            elif datetime.now() < qualistart:
                header = 'COMING UP NEXT :\n'
            elif datetime.now() < racestart:
                header = 'COMING UP NEXT :\n'
            elif datetime.now() < fp1end:
                header = 'CURRENTLY ON :\n'
            elif datetime.now() < fp2end:
                header = 'CURRENTLY ON :\n'
            elif datetime.now() < fp3end:
                header = 'CURRENTLY ON :\n'
            elif datetime.now() < qualiend:
                header = 'CURRENTLY ON :\n'
            elif datetime.now() < raceend:
                header = 'CURRENTLY ON :\n'
            return header"""

        def getHeader():
            if datetime.now() < fp1start:
                header = 'COMING UP NEXT :\n'
            elif datetime.now() < qualistart:
                header = 'COMING UP NEXT :\n'
            elif datetime.now() < fp2start:
                header = 'COMING UP NEXT :\n'
            elif datetime.now() < sprintstart:
                header = 'COMING UP NEXT :\n'
            elif datetime.now() < racestart:
                header = 'COMING UP NEXT :\n'
            elif datetime.now() < fp1end:
                header = 'CURRENTLY ON :\n'
            elif datetime.now() < qualiend:
                header = 'CURRENTLY ON :\n'
            elif datetime.now() < fp2end:
                header = 'CURRENTLY ON :\n'
            elif datetime.now() < sprintend:
                header = 'CURRENTLY ON :\n'
            elif datetime.now() < raceend:
                header = 'CURRENTLY ON :\n'
            return header

        def dateDiffInSeconds(date1, date2):
            timedelta = date2 - date1
            return timedelta.days * 24 * 3600 + timedelta.seconds

        def daysHoursMinutesSecondsFromSeconds(seconds):
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            return (days, hours, minutes, seconds)

        time_slot = getTime()
        time_header = getHeader()

        def getNextSlot(time_slot):
            if 'FP1' in time_slot:
                next_slot = fp1start
            elif 'Quali' in time_slot:
                next_slot = qualistart
            elif 'FP2' in time_slot:
                next_slot = fp2start
            elif 'Sprint' in time_slot:
                next_slot = sprintstart
            elif 'Race' in time_slot:
                next_slot = racestart
            return next_slot

        next_slot = getNextSlot(time_slot)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='--- ' + GP_name + ' ---' + '\n' + time_header + time_slot + '\n\n' +
                                 "In %d Days, %d Hr %d Min %d Sec" %
                                 daysHoursMinutesSecondsFromSeconds(dateDiffInSeconds(datetime.now(), next_slot)),
                            sender=Sender(
                                name='F1',
                                # name=None
                                icon_url='https://cdn.discordapp.com/attachments/813130040938201131/852629478923960350/dux4xq5v0zs41.png')

                        )
        )
        
        elif input_text == '首抽':
            
        wikiurl = "https://zh.wikipedia.org/wiki/%E5%90%84%E5%9B%BD%E5%AE%B6%E5%92%8C%E5%9C%B0%E5%8C%BA%E4%BA%BA%E5%8F%A3%E5%88%97%E8%A1%A8"
        table_class = "wikitable sortable jquery-tablesorter"
        response = requests.get(wikiurl)
        soup = BeautifulSoup(response.text, 'html.parser')
        worldtable = soup.find('table', {'class': "wikitable"})
        df = pd.read_html(str(worldtable))
        df = pd.DataFrame(df[0])
        df = df[['國家/地區', '佔世界比']]
        df.columns = ['country_old', 'percent']
        df = df[(df['country_old'] != '世界')]
        df['country'] = df['country_old'].str.split('[').str[0]
        df = df[['country', 'percent']]
        df['percent'] = df['percent'].str.strip()
        df['percent'] = df['percent'].str.replace('%', '')
        df['percent'] = df['percent'].str.replace("‰", "")
        df['percent'] = pd.to_numeric(df['percent'], errors='coerce')
        df['percent_new'] = df['percent'] / df['percent'].sum()

        draw = str(choice(df['country'].tolist(), 1, p=df.iloc[:, 2]))
        draw = draw.replace("'", '')
        draw = draw.replace("[", '')
        draw = draw.replace("]", '')

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='你下世做' + draw + '人啦^_^',
                            sender=Sender(
                                name='刷首抽轉盤',
                                # name=None
                                icon_url='https://cdn.discordapp.com/attachments/813130040938201131/889130450180784169/unknown.png')
                            )
                                )    
        
    else:
        def readtxt(filename):
            with open(filename) as f:
                lines = f.readlines()
                return lines

        prefix = readtxt('/prefix.txt')
        postfix_txt = readtxt('/postfix.txt')
        dark_postfix_txt = readtxt('/darklised_postfix.txt')

        postfix = [x.rstrip("\n") for x in postfix_txt]
        dark_postfix = [x.rstrip("\n") for x in dark_postfix_txt]

        blank_list = ['', '', '', '']
        ww = [' w', ' ww', ' www', ' wwww ', '', '', '', '']

        prefix_final = blank_list + prefix

        # For multipleline input text
        def finatext():
            test = input_text.split('\n')
            txtoutput_list = [x + random.choice(ww) + ' (' + random.choice(postfix) for x in test]
            finaloutput = "\n".join(txtoutput_list)

            return finaloutput

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random.choice(prefix_final) + finatext()))
