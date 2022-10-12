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
		cells(row) {
			return {
				className: row % 2 === 0 ? 'even' : 'odd',
			};
		},
		afterChange: (changes) => {
			changes?.forEach(([row, prop, oldValue, newValue]) => {
			});
		}, 
		licenseKey: 'non-commercial-and-evaluation'
	});
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
		cells(row) {
			return {
				className: row % 2 === 0 ? 'even' : 'odd',
			};
		},
		afterChange: (changes) => {
			changes?.forEach(([row, prop, oldValue, newValue]) => {
			});
		}, 
		licenseKey: 'non-commercial-and-evaluation'
	});
}