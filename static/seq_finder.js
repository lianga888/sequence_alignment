(function () {
  $("#find-sequence").submit(function(e) {
    e.preventDefault();

    var dna_sequence_name = $(this).find("input[name=dna_sequence_name]").val()
    var dna_sequence = $(this).find("textarea[name=dna_sequence]").val()
    var delay_s = $(this).find("input[name=delay_s]").val()
    $.ajax({
      url: "/find_dna_sequence",
      type: "post",
      contentType: "application/json",
      data: JSON.stringify({
        dna_sequence_name: dna_sequence_name,
        dna_sequence: dna_sequence,
        delay_s: delay_s,
      }),
      success: function () {
        alert("Success!")
        $("#find-sequence").find("input[type=text], textarea").val("");
      },
      error: function (req, status, error) {
        alert(JSON.parse(req.responseText)["err"])
      },
    });
  });

  function populate_results () {
    $.ajax({
      type: "post",
      url: "/get_latest_results",
      dataType: "json",
      success: function(response) {
        var $tbody = $("#latest-results").find("tbody");
        $tbody.empty();

        for (const row_data of response) {
          var id = row_data[0];
          var search_sequence_name = row_data[1];
          var matched_name = row_data[2];
          var matched_index = row_data[3];
          var href = `/get_searched_by_id/${id}`;

          var $tr = $("<tr>").append(
             $('<td>').text(id),
             $('<a class="seq-link">').text(
               search_sequence_name
             ).attr("href", href),
             $('<td>').text(matched_name === null ? "Not Found" : matched_name),
             $('<td>').text(matched_index === null ? "Not Found" : matched_index),
          );

          $tbody.append($tr)
        }
      }
    })
  }

  $("#latest-results").on("click", ".seq-link", function (e) {
    e.preventDefault();
    var url = e.currentTarget.href;
    $.ajax({
      type: "get",
      url: url,
      dataType: "json",
      success: function (response) {
        var search_sequence = response.search_sequence;
        $("#modal-text").text(search_sequence);
        $("#sequence-modal").show();
      }
    });
  });

  populate_results();
  setInterval(function () {
    populate_results();
  },10000);

  $("#close-btn").click( function() {
    $("#sequence-modal").hide();
  });
}());