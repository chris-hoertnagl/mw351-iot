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
        Watt_to_kWh = 60 * 1000
        cR_old_P += float(sm_input[1])/Watt_to_kWh
        cR_old_P1 += float(sm_input[2])/Watt_to_kWh
        cR_old_P2 += float(sm_input[3])/Watt_to_kWh
        cR_old_P3 += float(sm_input[4])/Watt_to_kWh

        with open("counterReading_all.txt", "w") as f:
            f.write(
                "counterReading_P:" + str(cR_old_P)+","
                "counterReading_P1:"+str(cR_old_P1)+","
                "counterReading_P2:"+str(cR_old_P2)+","
                "counterReading_P3:"+str(cR_old_P3)+","
            )
        payload_1 = {}
        payload_1["date"] = date
        payload_1["P"] = float(sm_input[1])
        payload_1["P1"] = float(sm_input[2])
        payload_1["P2"] = float(sm_input[3])
        payload_1["P3"] = float(sm_input[4])
        
        payload_2 = {}
        payload_2["date"] = date
        payload_2["I0"] = float(sm_input[5])
        payload_2["I1"] = float(sm_input[6])
        payload_2["I2"] = float(sm_input[7])
        payload_2["I3"] = float(sm_input[8])
        
        payload_3 = {}
        payload_3["date"] = date
        payload_3["V1"] = float(sm_input[9])
        payload_3["V2"] = float(sm_input[10])
        payload_3["V3"] = float(sm_input[11])

        payload_4 = {}
        payload_4["date"] = date
        payload_4["CR_P"] = cR_old_P

        payloads = [payload_1, payload_2, payload_3, payload_4]

        return payloads
    except:
        pass
