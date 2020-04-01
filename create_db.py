import app
import models

if __name__ == '__main__':
    chose = input('本次操作将会清空当前数据表，非常危险，是否操作[N]：')
    if not chose:
        exit()
    else:
        if chose != 'y' and chose != 'Y' and chose != 'N' and chose != 'n':
            exit()

        else:
            if chose == 'y' or chose == 'Y':
                app.db.drop_all()
                app.db.create_all()

