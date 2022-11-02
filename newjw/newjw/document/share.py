from background_task import background
from newjw.sharedoc.forms import sharePostForm, shareUserForm, shareDataCollectionForm, shareExcelJsonDataForm 
from newjw.sharedoc.models import post, user, data_collection, excel_json_data

def sharePostSave(*args, **kwargs):
    shareArr = args[0]
    form = sharePostForm(shareArr)

    if form.is_valid():
        record = form.save()
        return record.id
        
    return 0

# @background(schedule=1)
def shareExcelJsonDataSave(*args, **kwargs):
    shareArrJsonLoad = args[0]
    shareExcelform = shareExcelJsonDataForm(shareArrJsonLoad)

    if shareExcelform.is_valid():
        shareExcelform.save()
        
@background(schedule=1)
def shareDataCellSave(*args, **kwargs):

    id = args[0]
    excelJsonData = args[1]

    #데이터 셀 저장
    listexcelJsonData = list(excelJsonData)
    cell_row = 0
    cell_line = 0

    for forData in listexcelJsonData[0] :
        cell_row = cell_row+1
        cell_line = 0
        
        for rs in forData :
            
            cell_line = cell_line+1
            cell_type = "cell"
            if cell_row == 1 or cell_row == 2 :
                cell_type = "header"

            arrDataCollection = {"post":id,"cell_row":cell_row,"cell_line":cell_line,"data":rs,"cell_type":cell_type} 
            formDataCollection = shareDataCollectionForm(arrDataCollection)

            if formDataCollection.is_valid():
                formDataCollection.save()   