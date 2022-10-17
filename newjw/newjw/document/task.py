from background_task import background
from .models import post, data_collection, share_user, excel_json_data
    
@background(schedule=1)
def dataCellSave(id):
    print(id)
    # data = excel_json_data.objects.filter(post=id)
    # print(data)
    


    #데이터 셀 저장
    # listexcelJsonData = list(excelJsonData)
    # cell_row = 0
    # cell_line = 0

    # for forData in listexcelJsonData[0] :
    #     cell_row = cell_row+1
    #     cell_line = 0
    #     for rs in forData :
            
    #         cell_line = cell_line+1
    #         cell_type = "cell"
    #         if cell_row == 1 or cell_row == 2 :
    #             cell_type = "header"

    #         arrDataCollection = {"post":id,"cell_row":cell_row,"cell_line":cell_line,"data":rs,"cell_type":cell_type} 
    #         formDataCollection = dataCollectionForm(arrDataCollection)

    #         if formDataCollection.is_valid():
                
    #             #formDataCollection.save() 