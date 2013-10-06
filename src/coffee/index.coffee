# main object for storing state/whatever
Pynia = {
  histogramArea:
    height: 181
    width: 600
    x: 0
    y: 0
  spectographArea:
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
    " 06-09hz => ",
    " 09-12hz => ",
    " 12-15hz => ",
    " 15-20hz => ",
    " 20-25hz => ",
    " 25-30hz => "
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
  # add canvas for steps
  Pynia.canvas = $("#canvas")[0]
  Pynia.context = Pynia.canvas.getContext("2d")

  # set up a helper to draw the background
  Pynia.drawBackground = ->
    # fill background color
    Pynia.context.beginPath()
    Pynia.context.fillStyle = "#000630"
    Pynia.context.rect(
      Pynia.histogramArea.x,
      Pynia.histogramArea.y,
      Pynia.histogramArea.width,
      Pynia.histogramArea.height)
    Pynia.context.fill()

    Pynia.context.beginPath()
    Pynia.context.fillStyle = "white"
    Pynia.context.rect(
      Pynia.spectographArea.x,
      Pynia.spectographArea.y,
      Pynia.spectographArea.width,
      Pynia.spectographArea.height)
    Pynia.context.fill()

    Pynia.context.beginPath()
    Pynia.context.fillStyle = "black"
    Pynia.context.rect(
      Pynia.frequencyGraphArea.x,
      Pynia.frequencyGraphArea.y,
      Pynia.frequencyGraphArea.width,
      Pynia.frequencyGraphArea.height)
    Pynia.context.fill()

  Pynia.updateLoop = ->
    $.ajax
      url: "/get_steps"
      success: (response) ->
        $("#console").html("")

        # clear the canvas
        Pynia.drawBackground()

        _.each response.brain_fingers, (it, idx) ->
          # output the values of each frequency range to the console
          $("#console").append("#{Pynia.frequencyRangePrefixes[idx]} #{it}\n")

          # draw a moving historical line graph of each frequency range
          Pynia.frequencyHistories[idx].unshift(it)
          if (Pynia.frequencyHistories[idx].length > 410)
            Pynia.frequencyHistories[idx].pop()
          if (Pynia.frequencyHistories[idx].length > 1)
            Pynia.context.beginPath()
            Pynia.context.strokeStyle = "cyan"
            for i in [0..410]
              Pynia.context.moveTo(
                Pynia.frequencyGraphArea.x+(410-i),
                10 + Pynia.frequencyGraphArea.y + 20*idx + 10-Pynia.frequencyHistories[idx][i])
              Pynia.context.lineTo(
                Pynia.frequencyGraphArea.x+(410-(i+1)),
                10 + Pynia.frequencyGraphArea.y + 20*idx + 10-Pynia.frequencyHistories[idx][i+1])
            Pynia.context.stroke()

          # draw integer scale steps for each frequency range as a histogram
          if it >= 1
            for scale in [1..parseInt(it)]
              Pynia.context.drawImage(
                Pynia.stepImage,
                idx * 50 + 160,
                scale * -15 + 170)

        # redraw
        setTimeout ->
          Pynia.updateLoop()
        , 50

  Pynia.updateLoop()
