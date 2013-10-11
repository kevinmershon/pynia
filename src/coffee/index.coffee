# main object for storing state/whatever
Pynia = {
  brainFingers: [0,0,0,0,0,0]
  histogramArea:
    height: 181
    width: 600
    x: 0
    y: 0
  hexagonArea:
    height: 141
    width: 160
    x: 0
    y: 210
  frequencyGraphArea:
    height: 141
    width: 410
    x: 190
    y: 210
  frequencyRangePrefixes: [
    " (Alpha Low)  06-09hz => ",
    " (Alpha Med)  09-12hz => ",
    " (Alpha High) 12-15hz => ",
    " (Beta Low)   15-20hz => ",
    " (Beta Med)   20-25hz => ",
    " (Beta High)  25-30hz => "
  ]
  stepImage: new Image()
  frequencyHistories: [
    [],
    [],
    [],
    [],
    [],
    []
  ]
}

Pynia.stepImage.src = "/static/images/step.png"

$(document).ready ->
  Pynia.initializeGraphics()

  Pynia.updateLoop = ->
    $.ajax
      url: "/get_steps"
      success: (response) ->
        # output the values of each frequency range to the console
        $("#console").html("")
        _.each response.brain_fingers, (it, idx) ->
          $("#console").append("#{Pynia.frequencyRangePrefixes[idx]} #{it}\n")

        Pynia.brainFingers = response.brain_fingers

        # redraw
        setTimeout ->
          Pynia.updateLoop()
        , 50

  Pynia.updateLoop()
  Pynia.drawFrame()
