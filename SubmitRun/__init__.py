import logging
import azure.functions as func
import mechanize

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    br = mechanize.Browser()
    br.set_handle_robots( False )
    br.open("https://relief.jogno.net/login")

    br.select_form(nr=0)
    br["email"] = req_body.get('email')
    br["password"] = req_body.get('password')
    br.submit()

    page = br.open("https://relief.jogno.net/newnotes/")

    rundate = req_body.get('year') + '-' + req_body.get('month') + '-' + req_body.get('day')
    newurl = page.geturl() + '?d=' + rundate
    br.open(newurl)
    br.select_form(nr=0)
    try:
        temp = br.form.find_control(name="Jog[distance][]")
    except :
        req_body = req.get_json()
        br.form.new_control('text','Jog[distance][]',{'value':''})
        br.form.new_control('text','Jog[hour][]',{'value':''})
        br.form.new_control('text','Jog[minute][]',{'value':''})
        br.form.new_control('text','Jog[second][]',{'value':''})
        br.form.new_control('text','Jog[memo][]',{'value':''})
        br.form.fixup()

    br["Jog[distance][]"] = req_body.get('distance')
    br["Jog[hour][]"] = req_body.get('hour')
    br["Jog[minute][]"] = req_body.get('minute')
    br["Jog[second][]"] = req_body.get('second')
    br["diary"] = req_body.get('diary')
    br["Jog[memo][]"] = req_body.get('memo')
    # br["image_file[]"] = ""
    # br["condition[weight]"] = ""
    # print(br.form)
    br.submit()

    return func.HttpResponse(
        "This HTTP triggered function executed successfully.",
        status_code=200
    )
