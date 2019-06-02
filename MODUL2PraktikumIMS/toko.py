import pymysql
import time
import json
import os

FILE_NAME1 = './toko/' + 'last_seen_id.txt'
FILE_NAME = './bank/' + 'last_seen_id.txt'


def read_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def write_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def nama():
    last_seen_id = read_id(FILE_NAME)


def fileOperation(table, data, filename, operation):
    try:
        try:
            with open(filename, 'r') as f:
                try:
                    datajson = json.load(f)
                except:
                    datajson = {}
                    datajson[table] = []
        except:
            datajson = {}
            datajson[table] = []
        if (operation != "delete"):
            datajson[table].append({
                'operation': operation,
                'id_transaksi': str(data[0]),
                'no_rekening': str(data[1]),
                'tgl_transaksi': str(data[2]),
                'total_transaksi': str(data[3]),
                'status': str(data[4])
            })
        else:
            datajson[table].append({
                'operation': operation,
                'id_transaksi': str(data[0])
            })
        with open(filename, 'w') as outfile:
            json.dump(datajson, outfile)
    except (pymysql.Error, pymysql.Warning) as e:
        print(e)

    return 1


while (1):
    first_boot = 1
    try:
        connection_to_bank = 1

        try:
            connToko = pymysql.connect(host='localhost', user='root', passwd='', db='db_toko')
            curToko = connToko.cursor()
        except:
            print("can't connect to TOKO")

        try:
            connBank = pymysql.connect(host='localhost', user='root', passwd='', db='db_bank')
            curBank = connBank.cursor()

        except:
            print("can't connect to BANK")
            connection_to_bank = 0

        # read data dari json history toko saat first boot
        last_seen_bank = read_id(FILE_NAME)
        last_seen_toko = read_id(FILE_NAME1)
        counter = 0
        while (last_seen_toko <= last_seen_bank):
            baca = str(last_seen_toko)
            filepathtoko = './toko/' + "integrasi_toko" + baca + ".json"
            try:
                with open(filepathtoko, 'r') as f:
                    json_dict = json.load(f)
                    print('-- LOADING JSON FILE --')
                for jsonData in json_dict['tb_integrasi']:
                    if (jsonData['operation'] != 'delete'):
                        data = []
                        data.append(jsonData['id_transaksi'])
                        data.append(jsonData['no_rekening'])
                        data.append(jsonData['tgl_transaksi'])
                        data.append(jsonData['total_transaksi'])
                        data.append(jsonData['status'])

                        if (jsonData['operation'] == 'insert'):
                            val = (data[0], data[1], data[2], data[3], data[4])
                            insert_integrasi_toko = "insert into tb_integrasi (id_transaksi, no_rekening, tgl_transaksi, total_transaksi, status) values(%s,%s,%s,%s,%s)"
                            curToko.execute(insert_integrasi_toko, val)
                            connToko.commit()

                            insert_transaksi_toko = "insert into tb_transaksi (id_transaksi, no_rekening, tgl_transaksi, total_transaksi, status) values(%s,%s,%s,%s,%s)"
                            curToko.execute(insert_transaksi_toko, val)
                            connToko.commit()

                            print('- insert data from json file - id_transaksi = %s' % jsonData['id_transaksi'])

                        if (jsonData['operation'] == 'update'):
                            val = (data[1], data[2], data[3], data[4], data[0])
                            update_integrasi_toko = "update tb_integrasi set no_rekening = %s, tgl_transaksi = %s, total_transaksi = %s, status = %s where id_transaksi = %s"
                            curToko.execute(update_integrasi_toko, val)
                            connToko.commit()

                            update_transaksi_toko = "update tb_transaksi set no_rekening = %s, tgl_transaksi = %s, total_transaksi = %s, status = %s where id_transaksi = %s"
                            curToko.execute(update_transaksi_toko, val)
                            connToko.commit()

                            print('- update data from json file - id_transaksi = %s' % jsonData['id_transaksi'])
                    else:
                        data = []
                        data.append(jsonData['id_transaksi'])
                        val = (data[0])
                        delete_integrasi_toko = "delete from tb_integrasi where id_transaksi = %s"
                        curToko.execute(delete_integrasi_toko, val)
                        connToko.commit()

                        delete_transaksi_toko = "delete from tb_transaksi where id_transaksi = %s"
                        curToko.execute(delete_transaksi_toko, val)
                        connToko.commit()

                        print('- delete data from json file - %s ' % jsonData['id_transaksi'])

                os.remove(filepathtoko)
                write_id(baca, FILE_NAME1)
                print('-- DONE LOADING JSON FILE --')
            except:
                counter = 1
            last_seen_toko += 1
        # END

        sql_select = "SELECT * FROM tb_transaksi"
        curToko.execute(sql_select)
        result = curToko.fetchall()

        sql_select = "SELECT * FROM tb_integrasi"
        curToko.execute(sql_select)
        integrasi = curToko.fetchall()

        print("Listening...")

        # insert listener
        if (len(result) > len(integrasi)):
            print("-- INSERT DETECTED --")
            for data in result:
                a = 0
                for dataIntegrasi in integrasi:
                    if (data[0] == dataIntegrasi[0]):
                        a = 1
                if (a == 0):
                    print("-- RUN INSERT FOR ID = %s" % (data[0]))
                    val = (data[0], data[1], data[2], data[3], data[4])
                    insert_integrasi_toko = "insert into tb_integrasi (id_transaksi, no_rekening, tgl_transaksi, total_transaksi, status) values(%s,%s,%s,%s,%s)"
                    curToko.execute(insert_integrasi_toko, val)
                    connToko.commit()

                    if (connection_to_bank == 1):

                        last_seen_id = read_id(FILE_NAME1) + 1
                        nomer = str(last_seen_id)
                        filepathbank = './bank/' + "integrasi_bank" + nomer + ".json"
                        fileOperation("tb_integrasi", data, filepathbank, 'insert')
                        write_id(nomer, FILE_NAME1)

                    else:
                        last_seen_id = read_id(FILE_NAME1) + 1
                        nomer = str(last_seen_id)
                        filepathbank = './bank/' + "integrasi_bank" + nomer + ".json"
                        fileOperation("tb_integrasi", data, filepathbank, 'insert')
                        write_id(nomer, FILE_NAME1)
        # delete listener
        if (len(result) < len(integrasi)):
            print("-- DELETE DETECTED --")
            for dataIntegrasi in integrasi:
                a = 0
                for data in result:
                    if (dataIntegrasi[0] == data[0]):
                        a = 1
                if (a == 0):
                    print("-- RUN DELETE FOR ID = %s" % (dataIntegrasi[0]))

                    delete_integrasi_toko = "delete from tb_integrasi where id_transaksi = '%s'" % (dataIntegrasi[0])
                    curToko.execute(delete_integrasi_toko)
                    connToko.commit()

                    if (connection_to_bank == 1):
                        last_seen_id = read_id(FILE_NAME1) + 1
                        nomer = str(last_seen_id)
                        filepathbank = './bank/' + "integrasi_bank" + nomer + ".json"
                        fileOperation("tb_integrasi", dataIntegrasi, filepathbank, 'delete')
                        write_id(nomer, FILE_NAME1)
                    else:

                        last_seen_id = read_id(FILE_NAME1) + 1
                        nomer = str(last_seen_id)
                        filepathbank = './bank/' + "integrasi_bank" + nomer + ".json"
                        fileOperation("tb_integrasi", dataIntegrasi, filepathbank, 'delete')
                        write_id(nomer, FILE_NAME1)

        # update listener
        if (result != integrasi):
            print("-- EVENT SUCCESS OR UPDATE DETECTED --")
            for data in result:
                for dataIntegrasi in integrasi:
                    if (data[0] == dataIntegrasi[0]):
                        if (data != dataIntegrasi):
                            val = (data[1], data[2], data[3], data[4], data[0])
                            update_integrasi_toko = "update tb_integrasi set no_rekening = %s, tgl_transaksi = %s, total_transaksi = %s, status = %s where id_transaksi = %s"
                            curToko.execute(update_integrasi_toko, val)
                            connToko.commit()

                            if (connection_to_bank == 1):
                                last_seen_id = read_id(FILE_NAME1) + 1
                                nomer = str(last_seen_id)
                                filepathbank = './bank/' + "integrasi_bank" + nomer + ".json"
                                fileOperation("tb_integrasi", data, filepathbank, 'update')
                                write_id(nomer, FILE_NAME1)

                            else:

                                last_seen_id = read_id(FILE_NAME1) + 1
                                nomer = str(last_seen_id)
                                filepathbank = './bank/' + "integrasi_bank" + nomer + ".json"
                                fileOperation("tb_integrasi", data, filepathbank, 'update')
                                write_id(nomer, FILE_NAME1)

    except (pymysql.Error, pymysql.Warning) as e:
        print(e)

    # Untuk delay
    time.sleep(1)
