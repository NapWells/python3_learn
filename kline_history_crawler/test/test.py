if __name__ == '__main__':
    f = open(r'C:\Users\42515\Desktop\model_risk_user0109.csv')
    line = f.readline()
    w = open(r'C:\Users\42515\Desktop\model_risk_user.sql','w')
    sql = "INSERT INTO `model_risk_user` (`id`, `phone`, `risk_level`, `app`, `create_time`) VALUES ('{}', '{}', '{}', '{}', '{}');\n";
    while line:
        params = line.replace('\n','').split(',')
        # print("'" + line.replace('\n', '').replace(' ', '') + "'", end=',')
        w.writelines(sql.format(params[0],params[1],params[2],params[3],params[4]))

        line = f.readline()
    f.close()
    w.flush()
    w.close()


