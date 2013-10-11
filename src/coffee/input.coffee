Pynia.initializeInput = ->
  $("body").on "keydown", (e) ->
    switch e.which
      when 40, 74 # j/down
        eventType = "down_arrow"
      when 38, 75 # k/up
        eventType = "up_arrow"

    $.ajax
      url: "/log_event"
      data:
        event_type: eventType
      success:
        console.log("Event => #{eventType}")
