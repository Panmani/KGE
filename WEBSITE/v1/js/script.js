$(document).ready(function(e){
    // Submit form data via Ajax
    $("#input_form").on('submit', function(e){
      e.preventDefault();
      var formData = new FormData(this);
      console.log(formData)
      $.ajax({
          type: "POST",
          url: "/upload",
          data: formData,
          processData: false,
          contentType: false,
          success: function(r){
            console.log("result", r);
          },
          error: function (e) {
            alert(e.responseText);
          }
      });
    });


    var collData = {
        entity_types: [ {
                type   : 'Person',
                labels : ['Person', 'Per'],
                bgColor: '#7fa2ff',
                borderColor: 'darken'
        } ]
    };

    var docData = {
        text     : "Ed O'Kelley was the man who shot the man who shot Jesse James.",
        entities : [
            ['T1', 'Person', [[0, 11]]],
            ['T2', 'Person', [[20, 23]]],
            ['T3', 'Person', [[37, 40]]],
            ['T4', 'Person', [[50, 61]]],
        ],
        relations : [
            // Format: [${ID}, ${TYPE}, [[${ARGNAME}, ${TARGET}], [${ARGNAME}, ${TARGET}]]]
            ['R1', 'Anaphora', [['Person', 'T2'], ['Person', 'T1']]],
            ['R2', 'Anaphora', [['Person', 'T2'], ['Person', 'T3']]]
        ],
    };

    head.ready(function() {
        // Evaluate the code from the example (with ID
        // 'embedding-entity-example') and show it to the user
        Util.embed('SDP_graph', collData,
                docData, webFontURLs);
    });

    console.log("----------------------------------");

    var docData2 = {
        text     : "Ed O'Kelley was the man who shot the man who shot Jesse James.",
        entities : [
            ['T1', 'Person', [[0, 11]]],
            ['T2', 'Person', [[20, 23]]],
            ['T3', 'Person', [[37, 40]]],
            ['T4', 'Person', [[50, 61]]],
        ],
        relations : [
            // Format: [${ID}, ${TYPE}, [[${ARGNAME}, ${TARGET}], [${ARGNAME}, ${TARGET}]]]
            ['R1', 'Anaphora', [['Entity', 'T2'], ['Entity', 'T3']]]
        ],
    };

    var collData2 = {
        entity_types: [ {
                type   : 'Person',
                labels : ['Person', 'Per'],
                bgColor: '#7fa2ff',
                borderColor: 'darken'
        } ]
    };

    console.log(collData2);
    var dispatcher2;
    head.ready(function() {
        // Evaluate the code from the example (with ID
        // 'embedding-entity-example') and show it to the user
        dispatcher2 = Util.embed('NN_graph', collData2,
                docData2, webFontURLs);
    });

    // To update, run
    //     dispatcher2.post('requestRenderData', [docData2]);



});
