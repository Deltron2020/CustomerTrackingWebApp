table = new DataTable('#ticket_table', {
    paging: true
});

$(function() {
    $('a#search_button').on('click', function(e) {
        e.preventDefault()
        var ticketStatus = document.getElementById("TicketStatusSearch").value;
        var ticketType = document.getElementById("TicketTypeSearch").value;
        var ticketYear = document.getElementById("TicketYearSearch").value;
        var ticketNumber = document.getElementById("TicketNumberSearch").value;
        var ticketAccount = document.getElementById("AccountNumberSearch").value;
        var ticketDate = document.getElementById("ContactDateSearch").value;
        var ticketContact = document.getElementById("ContactTypeSearch").value;
        //var ticketReturnOperator = document.getElementById("ReturnOperatorSearch").value;
        var ticketOwner = document.getElementById("OwnerSearch").value;
        var ticketGotItOperator = document.getElementById("GotItOperatorSearch").value;
        var ticketCreator = document.getElementById("CreatedBySearch").value;
        var ticketDept = document.getElementById("DepartmentSearch").value;

        var searchCriteria = { Status : ticketStatus,
            TicketType : ticketType,
            TicketYear : ticketYear,
            TicketNumber : ticketNumber,
            AccountNumber : ticketAccount,
            ContactDate : ticketDate,
            ContactType : ticketContact,
            //ReturnOperator : ticketReturnOperator,
            OwnerName : ticketOwner,
            GotItUser : ticketGotItOperator,
            OriginalCreator : ticketCreator,
            Department : ticketDept
        }

        $.ajax({
            url: "/searchtestjson",
            type: "GET",
            dataType:"json",
            data: searchCriteria,
            success: function(data){
                //console.log(searchCriteria); // this is your response obj that you can work with

                table.clear();
                table.destroy();

                table = new DataTable('#ticket_table', {
                    columns: [
                        {data: 'TicketNumber'},
                        {data: 'ContactDate'},
                        {data: 'ContactType'},
                        {data: 'AccountNumber'},
                        {data: 'OwnerName'},
                        {data: 'ReturnOperator'},
                        {data: 'GotItUser'},
                        {data: 'Status'},
                    ],
                    columnDefs: [
                        {
                            targets: 0,
                            data: 'TicketNumber',
                            render: function (data, type, row, meta) {
                                data = '<a href="/search/' + data + '">' + data + '</a>';
                                return data;
                            },
                            width: '10%'
                        }
                    ]
                })

                table.rows.add(data);
                table.draw();

            }
        });

    });
    return false;
});


$(function() {
    $('a#clear_button').on('click', function(e) {
        e.preventDefault()
        document.getElementById("TicketStatusSearch").value = "";
        document.getElementById("TicketNumberSearch").value = "";
        document.getElementById("AccountNumberSearch").value = "";
        document.getElementById("ContactDateSearch").value = "";
        document.getElementById("ContactTypeSearch").value = "";
        //document.getElementById("ReturnOperatorSearch").value = "";
        document.getElementById("OwnerSearch").value = "";
        document.getElementById("GotItOperatorSearch").value = "";
        document.getElementById("CreatedBySearch").value = "";
        document.getElementById("DepartmentSearch").value = "";
    });
    return false;
});