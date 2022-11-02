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
		},
		afterSetCellMeta: (row, col, key, value) => {
			if (key === 'comment') {
			  
			}
		},
		licenseKey: 'non-commercial-and-evaluation'
	});

	$(container).find('table').addClass('table');
	$(container).find('table')['addClass']('table-striped');
	$(container).find('table')['addClass']('table-hover');
	update_setting(hot);
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
	 
	update_setting(hotObj[num]);
}

function setCellColor(key, opt) {
    let color = key.substring(6);
	
    for (let i = opt[0].start.row; i <= opt[0].end.row; i++) {
      for (let j = opt[0].start.col; j <= opt[0].end.col; j++) {
        this.getCell(i, j).style.color = color;
        this.setCellMeta(i, j, 'color', color); // Save the color
		
      }
    }
}

function setFont(key, opt) {
    let fontSize = key.substring(11);
    for (let i = opt[0].start.row; i <= opt[0].end.row; i++) {
      for (let j = opt[0].start.col; j <= opt[0].end.col; j++) {
        this.getCell(i, j).style.fontWeight= fontSize;
        this.setCellMeta(i, j, 'font', fontSize); // Save the color
      }
    }
}

function update_setting(obj){
	
	let cm = obj.getPlugin('ContextMenu');
	cm.open(1,1);
    obj.updateSettings({
        contextMenu: {
            items: Object.assign({}, cm.itemsFactory.predefinedItems,{
                'set_color': {
                    key: 'color',
                    name: '색상',
                    submenu: {
						"items": [{
							key: "color:white",
							"name": 'white<div class="white-dot"></div>',
							callback: setCellColor
						  }, {
							key: "color:red",
							name: 'red<div class="red-dot"></div>',
							callback: setCellColor
						  }, {
							key: "color:yellow",
							"name": 'yellow<div class="yellow-dot"></div>',
							callback: setCellColor
						  }, {
							key: "color:blue",
							name: 'blue<div class="blue-dot"></div>',
							callback: setCellColor
						  }, {
							key: "color:pink",
							name: 'pink<div class="pink-dot"></div>',
							callback:setCellColor
						  }, {
							key: "color:green",
							name: 'green<div class="green-dot"></div>',
							callback: setCellColor
						  }, {
							key: "color:black",
							name: 'black<div class="black-dot"></div>',
							callback: setCellColor
						  }
						  
						]
                    }
                },
                'set_font': {
                    key: 'fontweight',
                    name: '폰트',
                    submenu: {
                        items: [{
                            key: 'fontweight:700',
                            name: '진하게',
                            callback: setFont
                        }, {
                            key: 'fontweight:100',
                            name: '연하게',
                            callback: setFont
                        }]
                    }
                }
            })
        }
    })
    Handsontable.hooks.add('beforeRenderer', function(td, r, c, p, pv, cp){
        if (cp.color) {
            td.style.color = cp.color;
        }
		if (cp.background){
			td.style.background = cp.background
		}
    }, obj);
}