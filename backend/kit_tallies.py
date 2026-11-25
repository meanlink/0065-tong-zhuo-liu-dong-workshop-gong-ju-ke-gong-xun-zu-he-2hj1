def needs(lessons):
    return {"kits":sum(x["units"] for x in lessons),
            "minutes":sum(x["minutes"] for x in lessons),
            "tutors":sorted({x["tutor_key"] for x in lessons})}

def reconcile(stop,tally):
    missing=set(tally["tutors"])-set(stop["tutors"])
    return [label for exists,label in ((tally["kits"]>stop["kits"],"教具套数不足"),
            (tally["minutes"]>stop["duration"],"驻点时间不足"), (missing,"缺少教员 "+"/".join(sorted(missing)))) if exists]
