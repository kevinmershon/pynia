# main object for storing state/whatever
Pynia = {
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
    Pynia.context.fillStyle = "black"
    Pynia.context.rect(
      Pynia.hexagonArea.x,
      Pynia.hexagonArea.y,
      Pynia.hexagonArea.width,
      Pynia.hexagonArea.height)
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

        # draw a colored hexagonal shape using the frequency scales to mutate
        # the shape. redder is more beta (active), greener is more calm (alpha)
        baseSize = 20
        Xcenter = Pynia.hexagonArea.x + Pynia.hexagonArea.width/2
        Ycenter = Pynia.hexagonArea.y + Pynia.hexagonArea.height/2

        Pynia.context.beginPath()
        Pynia.context.moveTo(
          Xcenter + (baseSize+5*response.brain_fingers[5]) * Math.cos(6 * 2 * Math.PI / 6),
          Ycenter + (baseSize+5*response.brain_fingers[5]) * Math.sin(6 * 2 * Math.PI / 6))

        for i in [1..6]
          Pynia.context.lineTo(
            Xcenter + (baseSize+5*response.brain_fingers[i]) * Math.cos(i * 2 * Math.PI / 6),
            Ycenter + (baseSize+5*response.brain_fingers[i]) * Math.sin(i * 2 * Math.PI / 6))

        alphaSum = _.reduce(
          response.brain_fingers.slice(0, 3),
          (memo, it) ->
            memo + it
          , 0)
        betaSum = _.reduce(
          response.brain_fingers.slice(3, 6),
          (memo, it) ->
            memo + it
          , 0)
        blueishness = parseInt((60 - (alphaSum + betaSum)) / 60.0 * 255.0)
        greenishness = parseInt(alphaSum / 30.0 * 255.0)
        reddishness = parseInt(betaSum / 30.0 * 255.0)
        hexColor = (
          (reddishness << 16) +
          (greenishness << 8) +
          blueishness
        ).toString(16)
        hexColor = "000000".substring(0, 6-hexColor.length) + hexColor
        Pynia.context.fillStyle = "#" + hexColor
        Pynia.context.fill()


        # redraw
        setTimeout ->
          Pynia.updateLoop()
        , 50

  Pynia.updateLoop()
