### Initial setup script for the scholarship system
import argparse
import sys
import os
import xlrd
import xlwt
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scholarship.settings")
sys.path.append('../')
import django
import getpass
import hashlib
import json
django.setup()
from scholarship import settings
from dbapp.models import User,ApplyInfo

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file",help="input excel",type=str)
    if(len(sys.argv)==1):
        parser.print_help(sys.stderr)
        sys.exit(0)
    args = parser.parse_args()
    print("Opening file: {}".format(args.file))
    workbook = xlrd.open_workbook(filename=args.file)
    sheet0 = workbook.sheet_by_index(0)
    out = xlwt.Workbook(encoding='utf-8')
    wb_out = out.add_sheet('Result')
    line = 0
    for i in range(1, sheet0.nrows):
        stu_num = str(round(sheet0.cell_value(i,2)))
        score = float(sheet0.cell_value(i,13))
        #print("#{}: Student {}, extra score is {}".format(i,stu_num, score))
        try:
            user=User.objects.get(username=stu_num)
            apply_info=ApplyInfo.objects.get(user_id=user)
            res=json.loads(apply_info.json)
            if(res['other_academic'].find("PBokGE2nY2Qp8ukMBqqEFIFd5O3jc96V")>0):
                print("Student {} chose to use extra score {}".format(stu_num,round(score,2)))
                apply_info.extra_score=score
                apply_info.is_score_updated=False
                apply_info.save(force_update=True)
                wb_out.write(line,0,label=stu_num)
                line+=1
        except Exception as e:
            pass
    out.save("score_used.xls")

if(__name__=="__main__"):
   main()
