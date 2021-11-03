import datetime


def parse(data):
    try:
        sm_input = data[0].split("	")
        date = datetime.datetime.fromtimestamp(
            float(sm_input[0])).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        B = open("counterReading_all.txt", "r")
        file = B.read()
        current_stand = file.split(",")
        cR_old_P = float(current_stand[0].split(":")[1])
        cR_old_P1 = float(current_stand[1].split(":")[1])
        cR_old_P2 = float(current_stand[2].split(":")[1])
        cR_old_P3 = float(current_stand[3].split(":")[1])
        cR_old_P += float(sm_input[1])/3600
        cR_old_P1 += float(sm_input[2])/3600
        cR_old_P2 += float(sm_input[3])/3600
        cR_old_P3 += float(sm_input[4])/3600

        with open("counterReading_all.txt", "w") as f:
            f.write(
                "counterReading_P:" + str(cR_old_P)+","
                "counterReading_P1:"+str(cR_old_P1)+","
                "counterReading_P2:"+str(cR_old_P2)+","
                "counterReading_P3:"+str(cR_old_P3)+","
            )
        topic_1 = "EnergyMgmt/SM000001/Power"
        topic_2 = "EnergyMgmt/SM000001/Current"
        topic_3 = "EnergyMgmt/SM000001/Voltage"
        topic_4 = "EnergyMgmt/SM000001/CounterReading"
        payload_1 = "{date:"+date+", P:"+sm_input[1]+", P1:" + \
            sm_input[2]+", P2:"+sm_input[3]+", P3:"+sm_input[4]+"}"
        payload_2 = "{date:"+date+", I0:" + \
            sm_input[5]+", I1:"+sm_input[6]+", I2:" + \
            sm_input[7]+", I3:"+sm_input[8]+"}"
        payload_3 = "{date:"+date+", V1:" + \
            sm_input[9]+",V2:"+sm_input[10]+", V3:"+sm_input[11]+"}"
        payload_4 = "{date:"+date+", CR_P:" + \
            str(cR_old_P1 + cR_old_P2 + cR_old_P3)+"}"
        payloads = [payload_1, payload_2, payload_3, payload_4]
        topics = [topic_1, topic_2, topic_3, topic_4]

        return [topics, payloads]
    except:
        pass
