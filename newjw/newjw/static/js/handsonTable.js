function showExcelTable(container){
	hot = new Handsontable(container, {
		startRows: 20,
		startCols: 20,  
		width: 'auto',
		height: 'auto',
		rowHeaders: true,
		colHeaders: true,
		contextMenu: true,
		dropdownMenu: true,
		multiColumnSorting: true,
		filters: true,
		manualRowMove: true,  
		comments: true,
		language: 'ko-KR',
		mergeCells:[],
		fillHandle: true,
		// afterChange: (changes) => {
		// 	changes?.forEach(([row, prop, oldValue, newValue]) => {
		// 	});
		// }, 
		afterChange: function (change, source) {
			console.log(change)
		},
		licenseKey: 'non-commercial-and-evaluation'
	});

	$(container).find('table').addClass('table');
	$(container).find('table')['addClass']('table-striped');
	$(container).find('table')['addClass']('table-hover');
}

function showExcelTableObj(container,num){

	hotObj[num] = new Handsontable(container, {
		startRows: 20,
		startCols: 20,  
		width: 'auto',
		height: 'auto',
		rowHeaders: true,
		colHeaders: true,
		contextMenu: true,
		dropdownMenu: true,
		multiColumnSorting: true,
		filters: true,
		manualRowMove: true,  
		comments: true,
		language: 'ko-KR',
		mergeCells:[],
		fillHandle: true,
		afterChange: (changes) => {
			changes?.forEach(([row, prop, oldValue, newValue]) => {
			});
		}, 
		licenseKey: 'non-commercial-and-evaluation'
	});

	$(container).find('table').addClass('table');
	$(container).find('table')['addClass']('table-striped');
	$(container).find('table')['addClass']('table-hover');
}