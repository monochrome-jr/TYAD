function main_function(){
  
  // specify cells to be checked
  var cell_to_be_checked = [[3,3], [6,3], [9,3], [12,3], [15,3], [18,3], [21,3], [24,3],
                            [3,11], [6,11], [9,11], [12,11], [15,11], [18,11], [21,11], [24,11],
                            [3,17], [6,17], [9,17], [12,17], [15,17], [18,17], [21,17], [24,17]];
  
  // connect to current sheet
  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
  var current_sheet = sheets[0];
  
  // get date and month of today
  var today = new Date();
  var today_date = today.getDate();
  var today_month = today.getMonth();
  
  // iterate all specified cells
  for (var cellCount = 0; cellCount < cell_to_be_checked.length; cellCount++){
    
    // get date and month of cell value
    var cell_value = current_sheet.getRange(cell_to_be_checked[cellCount][0], cell_to_be_checked[cellCount][1]).getValues();
    var cell_date = new Date(cell_value).getDate();
    var cell_month = new Date(cell_value).getMonth();

    // comparison between today and cell, BUG WARNING -> DATE MAY BE NEGATIVE
    if (today_month == cell_month && today_date == cell_date - 1){
      
      // get required information
      var editor = current_sheet.getRange(cell_to_be_checked[cellCount][0] + 2, cell_to_be_checked[cellCount][1]).getValues();
      var reporter = current_sheet.getRange(cell_to_be_checked[cellCount][0], 1).getValues();
      var news = current_sheet.getRange(cell_to_be_checked[cellCount][0] + 1, cell_to_be_checked[cellCount][1]).getValues();
      
      // send email to editor
      if (editor == "菁"){
        MailApp.sendEmail("jing860424@gmail.com", "【青觀點】即時新聞通知！", reporter + " 的 " + news + " 新聞撰寫練習，要準備開寫囉！");
      }
      if (editor == "噴"){
        MailApp.sendEmail("emilythchen@gmail.com", "【青觀點】即時新聞通知！", reporter + " 的 " + news + " 新聞撰寫練習，要準備開寫囉！");
      }
      if (editor == "萌"){
        MailApp.sendEmail("alvin@taiwanyad.org", "【青觀點】即時新聞通知！", reporter + " 的 " + news + " 新聞撰寫練習，要準備開寫囉！");
      }
      if (editor == "Coco"){
        MailApp.sendEmail("coco.cheng@taiwanyad.org", "【青觀點】即時新聞通知！", reporter + " 的 " + news + " 新聞撰寫練習，要準備開寫囉！");
      }
    }
  }
}
