table = new DataTable('#sales_table', {
    paging: true
});

$(function() {
    $('a#search_button').on('click', function(e) {
        e.preventDefault()
        var beginDate = document.getElementById("BeginDateSearch").value;
        var endDate = document.getElementById("EndDateSearch").value;

        var searchCriteria = {
            begin : beginDate,
            end : endDate,
        }

        $.ajax({
            url: "/sales_report_json",
            type: "GET",
            dataType:"json",
            data: searchCriteria,
            success: function(data){
                //console.log(searchCriteria); // this is your response obj that you can work with

                table.clear();
                table.destroy();

                table = new DataTable('#sales_table', {
                    columns: [
                        {data: 'PropertyID'},
                        {data: 'SalesValidity'},
                        {data: 'SalesValidityDescription'},
                        {data: 'ExemptionCode'},
                        {data: 'ExemptionDescription'},
                        {data: 'ExemptionYearID'},
                        {data: 'GrantYear'},
                        {data: 'Tenancy'},
                        {data: 'SaleDateFormatted'},
                        {data: 'SalePriceFormatted'},
                        {data: 'FullBookPage'},
                        {data: 'RetainCapFlag'},
                        {data: 'GrantorName'},
                        {data: 'GranteeName'},
                    ],
                    layout: {
                        topStart: {
                            buttons: [
                                {
                                    extend: 'collection',
                                    text: 'Export',
                                    buttons: [
                                            {
                                                extend: 'copyHtml5',
                                                exportOptions: {
                                                columns: ':visible'
                                                }
                                            },
                                            {
                                                extend: 'excelHtml5',
                                                exportOptions: {
                                                columns: ':visible'
                                                }
                                            },
                                            {
                                                extend: 'csvHtml5',
                                                exportOptions: {
                                                columns: ':visible'
                                                }
                                            },
                                            {
                                                extend: 'pdfHtml5',
                                                orientation: 'landscape',
                                                exportOptions: {
                                                columns: ':visible'
                                                }
                                            }
                                        ]
                                },
                                {
                                    extend: 'colvis',
                                    text: 'Column Visibility',
                                },
                                {
                                    extend: 'pageLength'
                                },
                            ]
                        }
                    },
                    stateSave: true,
                    columnDefs: [
                        {
                            visible: true
                        }
                    ]
                })


                table.rows.add(data);
                table.draw();
                table.buttons.exportData({
                    columns: ':visible'
                });

            }
        });

    });
    return false;
});


$(function() {
    $('a#clear_button').on('click', function(e) {
        e.preventDefault()
        document.getElementById("BeginDateSearch").value = "";
        document.getElementById("EndDateSearch").value = "";
    });
    return false;
});