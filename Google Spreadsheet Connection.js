function get_data_from_sheet(sheet) {
  
  var last_row = sheet.getLastRow();
  
  var last_column = sheet.getLastColumn();
  
  var range = sheet.getRange(3, 1, last_row, last_column);
  
  var data = range.getValues();
  
  return data;
  
}


function update() {
  
  var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
  
  var summary_sheet = sheets[0];
  
  summary_sheet.deleteRows(3, summary_sheet.getLastRow());
  
  for (var sheet_name = 1; sheet_name < sheets.length; sheet_name++){
    
    var data = get_data_from_sheet(sheets[sheet_name]);
    
    for (var rowCount = 0; rowCount < data.length - 2; rowCount++){
      
     summary_sheet.appendRow( [ sheets[sheet_name].getName() ].concat( data[rowCount] ) );
      
    } 
    
  }
  
  // success message
  Browser.msgBox('今日事今日畢，早睡早起身體好');
  
}
