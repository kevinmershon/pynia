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
    Pynia.context.fillStyle = "#000630"
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

  Pynia.drawSteps = (steps) ->
    stepImage = new Image()
    stepImage.src = "/static/images/step.png"
    prefixes = [
      " 06-09hz => ",
      " 09-12hz => ",
      " 12-15hz => ",
      " 15-20hz => ",
      " 20-25hz => ",
      " 25-30hz => "
    ]

    $.ajax
      url: "/get_steps"
      success: (response) ->
        $("#console").html("")
        _.each response, (it, idx) ->
          $("#console").append("#{prefixes[idx]} #{it}\n")

          for height in [1..it]
            Pynia.context.drawImage(
              stepImage,
              idx * 50 + 160,
              height * -15 + 170)

        # redraw
        setTimeout ->
          Pynia.drawSteps()
        , 250

  Pynia.drawSteps()
