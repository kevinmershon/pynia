# main object for storing state/whatever
Pynia = {
  stepBlockArea:
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
}

$(document).ready ->
  # add canvas for steps
  Pynia.canvas = $("#canvas")[0]
  Pynia.context = Pynia.canvas.getContext("2d")

  # set up a helper to draw the background
  Pynia.drawBackground = ->
    # fill background color
    Pynia.context.beginPath()
    Pynia.context.fillStyle = "red"
    Pynia.context.rect(
      Pynia.stepBlockArea.x,
      Pynia.stepBlockArea.y,
      Pynia.stepBlockArea.width,
      Pynia.stepBlockArea.height)
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
    Pynia.context.fillStyle = "green"
    Pynia.context.rect(
      Pynia.frequencyGraphArea.x,
      Pynia.frequencyGraphArea.y,
      Pynia.frequencyGraphArea.width,
      Pynia.frequencyGraphArea.height)
    Pynia.context.fill()

  Pynia.drawBackground()
