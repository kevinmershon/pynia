Pynia.initializeGraphics = ->
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

  # set up a helper draw brainfingers
  Pynia.drawFrequencyHistorics = (brainFingers) ->
    _.each brainFingers, (it, idx) ->
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

  Pynia.drawHistogram = (brainFingers) ->
    _.each brainFingers, (it, idx) ->
      # draw integer scale steps for each frequency range as a histogram
      if it >= 1
        for scale in [1..parseInt(it)]
          Pynia.context.drawImage(
            Pynia.stepImage,
            idx * 50 + 160,
            scale * -15 + 170)

  Pynia.drawBrainShape = (brainFingers) ->
    # draw a colored hexagonal shape using the frequency scales to mutate
    # the shape. redder is more beta (active), greener is more calm (alpha)
    baseSize = 20
    Xcenter = Pynia.hexagonArea.x + Pynia.hexagonArea.width/2
    Ycenter = Pynia.hexagonArea.y + Pynia.hexagonArea.height/2

    Pynia.context.beginPath()
    Pynia.context.moveTo(
      Xcenter + (baseSize+5*brainFingers[5]) * Math.cos(6 * 2 * Math.PI / 6),
      Ycenter + (baseSize+5*brainFingers[5]) * Math.sin(6 * 2 * Math.PI / 6))

    for i in [1..6]
      Pynia.context.lineTo(
        Xcenter + (baseSize+5*brainFingers[i]) * Math.cos(i * 2 * Math.PI / 6),
        Ycenter + (baseSize+5*brainFingers[i]) * Math.sin(i * 2 * Math.PI / 6))

    alphaSum = _.reduce(
      brainFingers.slice(0, 3),
      (memo, it) ->
        memo + it
      , 0)
    betaSum = _.reduce(
      brainFingers.slice(3, 6),
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
