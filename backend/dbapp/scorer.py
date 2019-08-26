"""
Calculate score according to JSON config
"""
import json as JSON
import re
import dateutil.parser
import datetime
import sys
from dateutil import tz

class TimeValidator(object):
    def __init__(self, json):
        self.fmt = json['fmt']
        self.mode = json['mode']
        if(self.mode == 'regex'):
            self.pattern = re.compile(json['pattern'])
        elif(self.mode == 'regex+exp'):
            self.pattern = re.compile(json['pattern'])
            self.exp = json['exp']
        else:
            raise NotImplementedError("Unsupported mode in TimeValidator")
    def validate(self, __date, **kwargs):
        if(isinstance(__date, datetime.datetime)):
            __date = __date.strftime(self.fmt)
        else:
            print("Warning: you should pass datetime object to TimeValidator instead of str", file=sys.stderr)
        if(self.mode == 'regex'):
            return self.pattern.match(__date) is not None  ## return Not-None if matches
        elif(self.mode == 'regex+exp'):
            if(self.pattern.match(__date) is not None):
                ## check variables
                temp = self.exp
                for key, value in kwargs.items():
                    temp = temp.replace("$$" + key, str(value))
                    temp = temp.replace("$" + key, "'" + str(value) + "'")
                try:
                    return eval(temp)
                except Exception as e:
                    print(e)
                    print(temp)
                    return False
            else:
                return False
        else:
            raise NotImplementedError("Unsupported mode in TimeValidator")

class ItemScorer(object):
    def __init__(self, rules_dict, **kwargs):
        if('time_validator' in kwargs.keys()):
            if(not isinstance(kwargs['time_validator'], list)):
                raise TypeError("Invalid TimeValidator type, expected list")
            self.timeValidators = kwargs['time_validator']
        if('item_counter_rule' in kwargs.keys()):
            self.counter_mode = kwargs['item_counter_rule']['mode']
            if(self.counter_mode == "category"):
                self.counter_fmt = kwargs['item_counter_rule']['fmt']
                self.count = {}
                for item in kwargs['item_counter_rule']['fields']:
                    self.count[item] = 0
            elif(self.counter_mode == "count"):
                self.count = 0
                pass
            else:
                raise NotImplementedError("Unsupported counter mode in ItemScorer")
        self.time_field = rules_dict['time_field']
        self.mode = rules_dict['mode']
        if('limit' in rules_dict.keys()):
            self.limit = rules_dict['limit']
        if(self.mode == 'lut'):
            self.fmt = rules_dict['fmt']
            self.lut = rules_dict['lut']
        elif(self.mode == 'value'):
            self.formula = rules_dict['formula']
        else:
            raise NotImplementedError("Unsupported mode in ItemScorer")

    def __validateTime(self, __date, **kwargs):
        if(not hasattr(self, 'timeValidators') or len(self.timeValidators) == 0):
            return True
        else:
            for validator in self.timeValidators:
                if(validator.validate(__date, **kwargs)):
                    return True
            return False

    def __formulaReplacer(self, string, **kwargs):
        for key, value in kwargs.items():
            string = string.replace("$$" + key, str(value))
            string = string.replace("$" + key, "'" + str(value) + "'")
        return string

    def getScore(self, item_list):
        if(hasattr(self, 'counter_mode')):
            if(isinstance(self.count, int)):
                self.count = 0
            elif(isinstance(self.count, dict)):
                for k in self.count.keys():
                    self.count[k] = 0
        if(not isinstance(item_list, list)):
            raise TypeError("Invalid item list, expected list type")
        tot_score = 0.0
        wrong_time = False
        if(self.mode == 'value'):
            cnt = 0
            for item in item_list:
                flag = False
                for field in self.time_field:
                    d = dateutil.parser.parse(item[field]).astimezone(tz.tzlocal())
                    if(not self.__validateTime(d, **item)):
                        wrong_time = True
                        flag = True
                        break
                if(flag):
                    continue
                if(hasattr(self, 'counter_mode')):
                    # begin count
                    if(self.counter_mode == "count"):
                        self.count += 1
                    elif(self.counter_mode == "category"):
                        t = self.__formulaReplacer(self.counter_fmt, **item)
                        if(t in self.count.keys()):
                            self.count[t] += 1
                cnt += 1
            if(cnt > 0):
                try:
                    temp = self.__formulaReplacer(self.formula, **item)
                    tot_score += eval(temp)
                except Exception as e:
                    print(e)
        else:
            typed_score = {}
            for item in item_list:
                flag = False
                for field in self.time_field:
                    d = dateutil.parser.parse(item[field]).astimezone(tz.tzlocal())
                    if(not self.__validateTime(d, **item)):
                        wrong_time = True
                        flag = True
                        break
                if(flag):
                    continue
                else:
                    if(hasattr(self, 'counter_mode')):
                        # begin count
                        if(self.counter_mode == "count"):
                            self.count += 1
                        elif(self.counter_mode == "category"):
                            t = self.__formulaReplacer(self.counter_fmt, **item)
                            if(t in self.count.keys()):
                                self.count[t] += 1
                    if(self.mode == 'lut'):
                        pat = self.__formulaReplacer(self.fmt, **item)
                        if(pat in self.lut.keys()):
                            score_obj = self.lut[pat]
                            score_expr = self.__formulaReplacer(score_obj['formula'], **item)
                            try:
                                score = eval(score_expr)
                                if(pat not in typed_score.keys()):
                                    typed_score[pat] = score
                                else:
                                    typed_score[pat] += score
                            except Exception as e:
                                print(e)
                    else:
                        raise NotImplementedError("Unsupported mode")
            if(self.mode == 'lut'):
                for k,v in typed_score.items():
                    if('limit' in self.lut[k].keys()):
                        lim = eval(self.lut[k]['limit'])
                        tot_score += min(lim, v)
                    else:
                        tot_score += v
        if(hasattr(self, 'limit')):
            tot_score = min(tot_score, eval(self.limit))
        if(hasattr(self, 'counter_mode')):
            return tot_score, (wrong_time, self.count)
        else:
            return tot_score, wrong_time

class ScoreCalculator(object):
    def __formulaReplacer(self, string, **kwargs):
        for key, value in kwargs.items():
            string = string.replace("$$" + key, str(value))
            string = string.replace("$" + key, "'" + str(value) + "'")
        return string
    def __init__(self, rule_dict):
        print("Initializing scorer...")
        self.timeValidators = []
        if('time_validator' in rule_dict.keys()):
            for item in rule_dict['time_validator']:
                self.timeValidators.append(TimeValidator(item))
        self.academic_scorer = {}
        self.work_scorer = {}
        self.final_formula = rule_dict['total']['formula']
        self.has_counter = ('item_counter' in rule_dict.keys())
        if(self.has_counter):
            self.counter_dict = rule_dict['item_counter']
        for key, item in rule_dict['academic'].items():
            time_validator = self.timeValidators if 'time_validator_filter' not in item.keys() else []
            if('time_validator' in rule_dict.keys() and 'time_validator_filter' in item.keys()):
                for idx in item['time_validator_filter']:
                    time_validator.append(self.timeValidators[idx])
            if('item_counter' in rule_dict.keys() and 'academic' in rule_dict['item_counter'].keys()
                and key in rule_dict['item_counter']['academic'].keys()):
                self.academic_scorer[key] = ItemScorer(item, time_validator=time_validator, item_counter_rule=rule_dict['item_counter']['academic'][key])
            else:
                self.academic_scorer[key] = ItemScorer(item, time_validator=time_validator)

        for key, item in rule_dict['work'].items():
            time_validator = self.timeValidators if 'time_validator_filter' not in item.keys() else []
            if('time_validator' in rule_dict.keys() and 'time_validator_filter' in item.keys()):
                for idx in item['time_validator_filter']:
                    time_validator.append(self.timeValidators[idx])
            if('item_counter' in rule_dict.keys() and 'work' in rule_dict['item_counter'].keys()
                and key in rule_dict['item_counter']['work'].keys()):
                self.work_scorer[key] = ItemScorer(item, time_validator=time_validator, item_counter_rule=rule_dict['item_counter']['work'][key])
            else:
                self.work_scorer[key] = ItemScorer(item, time_validator=time_validator)
        print("Scorer initialization done...")
            

    def getScore(self, item_dict):
        ## academic_score
        academic = 0.0
        counter_res = {'academic': {}, 'work': {}}
        wrong_time = False
        for key, item in item_dict['academic'].items():
            score, _ = self.academic_scorer[key].getScore(item)
            academic += score
            if(self.has_counter and 'academic' in self.counter_dict.keys() and key in self.counter_dict['academic'].keys()):
                counter_res['academic'][key] = _[1]
                if(_[0]):
                    wrong_time = True
            elif(_):
                wrong_time = True
        work = 0.0
        for key, item in item_dict['work'].items():
            score, _ = self.work_scorer[key].getScore(item)
            work += score
            if(self.has_counter and 'work' in self.counter_dict.keys() and key in self.counter_dict['work'].keys()):
                counter_res['work'][key] = _[1]
                if(_[0]):
                    wrong_time = True
            elif(_):
                wrong_time = True
        formula = self.__formulaReplacer(self.final_formula, academic=academic, work=work)
        try:
            return eval(formula), academic, work, counter_res, wrong_time
        except Exception as e:
            print(e)
            return 0.0, academic, work, counter_res, wrong_time


"""
Unit test
"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

if(__name__ == "__main__"):
    ### TEST ITEM_SCORER
    print("Start Unit Test")
    tValidatorJson = "{\"time_validator\":[{\"mode\":\"regex\",\"fmt\":\"%Y-%m\",\"pattern\":\"201(7-(09|1[0-2])|8-0[1-8])\"},{\"mode\":\"regex+exp\",\"fmt\":\"%Y-%m\",\"pattern\":\"201(8-08|9-.*?)\",\"exp\":\"$isLastYear=='1'\"}]}"
    tValidator = JSON.loads(tValidatorJson)
    tValidator = [TimeValidator(tValidator['time_validator'][0]), TimeValidator(tValidator['time_validator'][1])]
    def test1():
        scorerJson = "{\"mode\":\"lut\",\"time_field\":[\"date\"],\"fmt\":\"$$ccfRank-$$category-$$isFirstAuthor\",\"lut\":{\"A-full-1\":{\"formula\":\"5\"},\"B-full-1\":{\"formula\":\"3\"},\"C-full-1\":{\"formula\":\"1.5\"},\"O-full-1\":{\"formula\":\"1\",\"limit\":\"1\"}}}"
        scorerRule = JSON.loads(scorerJson)
        scorer = ItemScorer(scorerRule, time_validator=tValidator)
        itemsJson = "[{\"seq\":\"0\",\"author\":\"sss\",\"isFirstAuthor\":\"0\",\"ccfRank\":\"A\",\"journal\":\"\",\"paper\":\"sss\",\"date\":\"2017-10-31T16:00:00.000Z\",\"numPages\":\"1\",\"category\":\"full\",\"isLastYear\":\"0\",\"conf\":\"sss\"},{\"seq\":\"1\",\"author\":\"sss\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"B\",\"journal\":\"\",\"paper\":\"sss\",\"date\":\"2017-10-31T16:00:00.000Z\",\"numPages\":\"1\",\"category\":\"full\",\"isLastYear\":\"0\",\"conf\":\"sss\"},{\"seq\":\"2\",\"author\":\"sss\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"O\",\"journal\":\"\",\"paper\":\"sss\",\"date\":\"2017-10-31T16:00:00.000Z\",\"numPages\":\"1\",\"category\":\"full\",\"isLastYear\":\"0\",\"conf\":\"sss\"},{\"seq\":\"3\",\"author\":\"sss\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"O\",\"journal\":\"\",\"paper\":\"sss\",\"date\":\"2017-10-31T16:00:00.000Z\",\"numPages\":\"1\",\"category\":\"full\",\"isLastYear\":\"0\",\"conf\":\"sss\"},{\"seq\":\"4\",\"author\":\"sss\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"C\",\"journal\":\"\",\"paper\":\"sss\",\"date\":\"2019-10-31T16:00:00.000Z\",\"numPages\":\"1\",\"category\":\"full\",\"isLastYear\":\"1\",\"conf\":\"sss\"},{\"seq\":\"5\",\"author\":\"sss\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"B\",\"journal\":\"\",\"paper\":\"sss\",\"date\":\"2019-10-31T16:00:00.000Z\",\"numPages\":\"1\",\"category\":\"full\",\"isLastYear\":\"0\",\"conf\":\"sss\"}]"
        items = JSON.loads(itemsJson)
        score, wrong_time = scorer.getScore(items)
        assert(score == 5.5 and wrong_time == True)
        print("Pass")
    def test2():
        scorerJson = "{\"mode\":\"value\",\"time_field\":[\"date\"],\"formula\":\"2\"}"
        scorerRule = JSON.loads(scorerJson)
        scorer = ItemScorer(scorerRule, time_validator=tValidator)
        itemsJson = "[{\"seq\":\"0\",\"author\":\"ss\",\"name\":\"sss\",\"date\":\"2019-07-31T16:00:00.000Z\",\"isLastYear\":\"1\"},{\"seq\":\"0\",\"author\":\"ss\",\"name\":\"sss\",\"date\":\"2019-07-31T16:00:00.000Z\",\"isLastYear\":\"1\"}]"
        items = JSON.loads(itemsJson)
        score, wrong_time = scorer.getScore(items)
        assert(score == 2 and wrong_time == False)
        print("Pass")
    def test3():
        scorerJson = "{\"mode\":\"value\",\"time_field\":[\"date\"],\"formula\":\"2\"}"
        scorerRule = JSON.loads(scorerJson)
        scorer = ItemScorer(scorerRule, time_validator=tValidator)
        itemsJson = "[]"
        items = JSON.loads(itemsJson)
        score, wrong_time = scorer.getScore(items)
        assert(score == 0 and wrong_time == False)
        print("Pass")
    def test4():
        scorerJson = "{\"mode\":\"value\",\"time_field\":[\"date\"],\"formula\":\"2\"}"
        scorerRule = JSON.loads(scorerJson)
        scorer = ItemScorer(scorerRule, time_validator=tValidator)
        itemsJson = "[{\"seq\":\"0\",\"author\":\"ss\",\"name\":\"sss\",\"date\":\"2019-07-31T16:00:00.000Z\",\"isLastYear\":\"1\"},{\"seq\":\"0\",\"author\":\"ss\",\"name\":\"sss\",\"date\":\"2019-07-31T16:00:00.000Z\",\"isLastYear\":\"1\"},{\"seq\":\"0\",\"author\":\"ss\",\"name\":\"sss\",\"date\":\"2019-07-31T16:00:00.000Z\",\"isLastYear\":\"1\"},{\"seq\":\"0\",\"author\":\"ss\",\"name\":\"sss\",\"date\":\"2019-07-31T16:00:00.000Z\",\"isLastYear\":\"1\"}]"
        items = JSON.loads(itemsJson)
        score, wrong_time = scorer.getScore(items)
        assert(score == 2 and wrong_time == False)
        print("Pass")
    def test5():
        scorerJson = "{\"mode\":\"lut\",\"time_field\":[\"startDate\",\"endDate\"],\"fmt\":\"$$class\",\"lut\":{\"A\":{\"formula\":\"5 * (min($$monthFirst, 4) + min($$monthSecond, 4))/ 8.0\"},\"B\":{\"formula\":\"4 * (min($$monthFirst, 4) + min($$monthSecond, 4))/ 8.0\"},\"C\":{\"formula\":\"3 * (min($$monthFirst, 4) + min($$monthSecond, 4))/ 8.0\"},\"D\":{\"formula\":\"1 * (min($$monthFirst, 4) + min($$monthSecond, 4))/ 8.0\"}}}"
        scorerRule = JSON.loads(scorerJson)
        itemJson = "[{\"seq\":\"0\",\"name\":\"ss\",\"class\":\"A\",\"startDate\":\"2017-09-30T16:00:00.000Z\",\"endDate\":\"2017-09-08T16:00:00.000Z\",\"monthFirst\":12,\"monthSecond\":2},{\"seq\":\"0\",\"name\":\"ss\",\"class\":\"B\",\"startDate\":\"2017-09-30T16:00:00.000Z\",\"endDate\":\"2017-09-08T16:00:00.000Z\",\"monthFirst\":2,\"monthSecond\":5},{\"seq\":\"0\",\"name\":\"ss\",\"class\":\"C\",\"startDate\":\"2019-09-30T16:00:00.000Z\",\"endDate\":\"2019-09-08T16:00:00.000Z\",\"monthFirst\":2,\"monthSecond\":2}]"
        items = JSON.loads(itemJson)
        scorer = ItemScorer(scorerRule, time_validator=tValidator[0:1])
        score, wrong_time = scorer.getScore(items)
        assert(score == 6.75 and wrong_time == True)
        print("Pass")
    def test6():
        scorerJson = "{\"mode\":\"lut\",\"limit\":\"3\",\"time_field\":[\"startDate\",\"endDate\"],\"fmt\":\"$$class\",\"lut\":{\"A\":{\"formula\":\"5 * (min($$monthFirst, 4) + min($$monthSecond, 4))/ 8.0\"},\"B\":{\"formula\":\"4 * (min($$monthFirst, 4) + min($$monthSecond, 4))/ 8.0\"},\"C\":{\"formula\":\"3 * (min($$monthFirst, 4) + min($$monthSecond, 4))/ 8.0\"},\"D\":{\"formula\":\"1 * (min($$monthFirst, 4) + min($$monthSecond, 4))/ 8.0\"}}}"
        scorerRule = JSON.loads(scorerJson)
        itemJson = "[{\"seq\":\"0\",\"name\":\"ss\",\"class\":\"A\",\"startDate\":\"2017-09-30T16:00:00.000Z\",\"endDate\":\"2017-09-08T16:00:00.000Z\",\"monthFirst\":12,\"monthSecond\":2},{\"seq\":\"0\",\"name\":\"ss\",\"class\":\"B\",\"startDate\":\"2017-09-30T16:00:00.000Z\",\"endDate\":\"2017-09-08T16:00:00.000Z\",\"monthFirst\":2,\"monthSecond\":5}]"
        items = JSON.loads(itemJson)
        scorer = ItemScorer(scorerRule, time_validator=tValidator[0:1])
        score, wrong_time = scorer.getScore(items)
        assert(score == 3 and wrong_time == False)
        print("Pass")
    executor = ThreadPoolExecutor(max_workers=6)
    executor.submit(test1)
    executor.submit(test2)
    executor.submit(test3)
    executor.submit(test4)
    executor.submit(test5)
    executor.submit(test6)
    executor.shutdown(True)
    if(len(sys.argv) == 1):
        print("No input JSON specific, exit")
        sys.exit(0)
    with open(sys.argv[1], "r") as f:
        rule = JSON.load(f)
        rule = rule['score_rule_settings']['json_debug']
        rule = JSON.loads(rule)
        scorer = ScoreCalculator(rule)
        itemJson = "{\"academic\":{\"conf_paper\":[{\"seq\":\"0\",\"author\":\"aaa\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"A\",\"journal\":\"\",\"paper\":\"aaaa\",\"date\":\"2017-04-30T16:00:00.000Z\",\"numPages\":\"1\",\"category\":\"full\",\"isLastYear\":\"1\",\"conf\":\"aaaa\"},{\"seq\":\"1\",\"author\":\"aaaa\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"B\",\"journal\":\"\",\"paper\":\"aaa\",\"date\":\"2016-06-08T16:00:00.000Z\",\"numPages\":\"1\",\"category\":\"full\",\"isLastYear\":\"0\",\"conf\":\"aaa\"},{\"seq\":\"2\",\"author\":\"aaaa\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"B\",\"journal\":\"\",\"paper\":\"aaa\",\"date\":\"2018-06-06T16:00:00.000Z\",\"numPages\":\"1\",\"category\":\"full\",\"isLastYear\":\"0\",\"conf\":\"aaa\"},{\"seq\":\"3\",\"author\":\"aaa\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"B\",\"journal\":\"\",\"paper\":\"aaa\",\"date\":\"2017-06-13T16:00:00.000Z\",\"numPages\":\"1\",\"category\":\"short\",\"isLastYear\":\"0\",\"conf\":\"aaa\"}],\"journal_paper\":[{\"seq\":\"0\",\"author\":\"aaa\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"A\",\"journal\":\"aa\",\"paper\":\"aaaa\",\"date\":\"2018-05-02T16:00:00.000Z\",\"pagePos\":\"1\",\"numPages\":\"2\",\"category\":\"full\",\"isLastYear\":\"1\"},{\"seq\":\"1\",\"author\":\"a\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"A\",\"journal\":\"aaa\",\"paper\":\"aa\",\"date\":\"2018-12-22T16:00:00.000Z\",\"pagePos\":\"1\",\"numPages\":\"1\",\"category\":\"full\",\"isLastYear\":\"1\"},{\"seq\":\"2\",\"author\":\"v\",\"isFirstAuthor\":\"1\",\"ccfRank\":\"A\",\"journal\":\"aaaa\",\"paper\":\"aaa\",\"date\":\"2019-04-21T16:00:00.000Z\",\"pagePos\":\"1\",\"numPages\":\"1\",\"category\":\"full\",\"isLastYear\":\"1\"}],\"patent\":[],\"project\":[],\"intl_standard\":[],\"conf_award\":[]},\"work\":{\"post\":[{\"seq\":\"0\",\"name\":\"aaaaaaa\",\"class\":\"D\",\"startDate\":\"2015-03-10T16:00:00.000Z\",\"endDate\":\"2015-08-12T16:00:00.000Z\",\"monthFirst\":0,\"monthSecond\":6},{\"seq\":\"1\",\"name\":\"a\",\"class\":\"D\",\"startDate\":\"2015-09-15T16:00:00.000Z\",\"endDate\":\"2016-08-29T16:00:00.000Z\",\"monthFirst\":6,\"monthSecond\":6},{\"seq\":\"2\",\"name\":\"a\",\"class\":\"D\",\"startDate\":\"2016-09-04T16:00:00.000Z\",\"endDate\":\"2017-08-29T16:00:00.000Z\",\"monthFirst\":6,\"monthSecond\":6},{\"seq\":\"3\",\"name\":\"a\",\"class\":\"D\",\"startDate\":\"2017-09-17T16:00:00.000Z\",\"endDate\":\"2018-08-16T16:00:00.000Z\",\"monthFirst\":6,\"monthSecond\":6}],\"accu_pro\":[{\"seq\":\"0\",\"class\":\"H\",\"content\":\"bbbbbbbbbbbbbbb\",\"date\":\"2014-12-11T16:00:00.000Z\"},{\"seq\":\"1\",\"class\":\"L\",\"content\":\"aa\",\"date\":\"2018-09-16T16:00:00.000Z\"},{\"seq\":\"2\",\"class\":\"L\",\"content\":\"a\",\"date\":\"2017-09-11T16:00:00.000Z\"},{\"seq\":\"3\",\"class\":\"L\",\"content\":\"aa\",\"date\":\"2016-05-11T16:00:00.000Z\"},{\"seq\":\"4\",\"class\":\"L\",\"content\":\"aaa\",\"date\":\"2015-04-07T16:00:00.000Z\"}]},\"other_academic\":\"aaaaaaaaaaaaaa\"}"
        items = JSON.loads(itemJson)
        score_res = scorer.getScore(items)
        print(score_res)