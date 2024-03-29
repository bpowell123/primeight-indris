      var fsec = pv.Format.date("%S s"),
          fmin = pv.Format.date("%M m"),
          fhou = pv.Format.date("%H h"),
          fwee = pv.Format.date("%a"),
          fdat = pv.Format.date("%d d"),
          fmon = pv.Format.date("%b"),
          radius = 768 / 2;

      /* Generate the fields for the given date. */
      function fields() {
        var d = new Date();

        function days() {
          return 32 - new Date(d.getYear(), d.getMonth(), 32).getDate();
        }

        var second = (d.getSeconds() + d.getMilliseconds() / 1000) / 60;
        var minute = (d.getMinutes() + second) / 60;
        var hour = (d.getHours() + minute) / 24;
        var weekday = (d.getDay() + hour) / 7;
        var date = (d.getDate() - 1 + hour) / days();
        var month = (d.getMonth() + date) / 12;

        return [
            { value: second,  index: .7, text: fsec(d) },
            { value: minute,  index: .6, text: fmin(d) },
            { value: hour,    index: .5, text: fhou(d) },
            { value: weekday, index: .3, text: fwee(d) },
            { value: date,    index: .2, text: fdat(d) },
            { value: month,   index: .1, text: fmon(d) },
          ];
      }

      var vis = new pv.Panel()
          .width(radius * 2)
          .height(radius * 2);

      vis.add(pv.Wedge)
          .data(fields)
          .left(radius)
          .bottom(radius)
          .innerRadius(function(d) radius * d.index)
          .outerRadius(function(d) radius * (d.index + .1))
          .startAngle(-Math.PI / 2)
          .angle(function(d) 2 * Math.PI * d.value)
          .fillStyle(function(d) "hsl(" + (360 * d.value - 180) + ", 50%, 50%)")
          .lineWidth(4)
          .strokeStyle("#222")
        .anchor("end").add(pv.Label)
          .font("bold 12px sans-serif")
          .textStyle("#000")
          .textMargin(7)
          .text(function(d) d.text);

      setInterval(function() vis.render(), 50);