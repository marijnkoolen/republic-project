import * as d3 from 'd3';
import {MutableRefObject} from 'react';
import heatmapTestdata from './heatmap-testdata.json';

export function renderHeatmap(
  canvasRef: MutableRefObject<any>,
  // bars: HistogramBar[],
  // config: HistogramConfig,
  // handleBarClick: (ids: string[]) => void
) {

  const data = heatmapTestdata;

  let result = new Map(data.map(value => [value['date'], value['count']]));

  const start = data[0].date;
  const startDate = new Date(start);

  const end = data[data.length - 1].date;
  const endDate = new Date(end);

  const svgSize = canvasRef.current.getBoundingClientRect();
  const height = svgSize.height;
  const width = svgSize.width;

  const startMonthDate = new Date(startDate);
  startMonthDate.setDate(0);
  const monthRange = d3.timeMonth.range(startMonthDate, endDate);

  const margin = {top: 20, right: 30, bottom: 20, left: 20};

  const cellWidth = (width - margin.left - monthRange.length * 2) / (result.size / 7);
  const cellHeight = height / 8;

  const color = d3.scaleQuantize<string>()
    .domain([0, 100])
    .range(['#f3f6e7', '#e7eecf', '#dbe5b7', '#d0dd9f', '#c4d587', '#b8cd6f', '#acc457', '#a1bc3f', '#94b327', '#89ab0f']);
  const svg = d3.select(canvasRef.current)
    .select(".d3-canvas")
    .select(".plot-area")
    .data([parseInt(start)])
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', `translate(${margin.left},1)`);

  svg.append('g')
    .attr('fill', 'none')
    .attr('stroke', '#000')
    .attr('stroke-width', '0.1px')
    .selectAll('rect')
    .data(() => {
      let startDateEdge = new Date(startDate);
      startDateEdge.setDate(startDate.getDate() - 1)
      return d3.timeDays(startDateEdge, endDate);
    })
    .enter()
    .append('rect')
    .attr('width', cellWidth)
    .attr('height', cellHeight)
    .attr('x', d => d3.timeMonday.count(startDate, d) * cellWidth)
    .attr('y', d => d.getUTCDay() * cellHeight)
    .datum(d3.timeFormat('%Y-%m-%d'))
    .attr('fill', d => color(result.get(d) as number))
    .on('mouseover', function (e, d) {
      d3.select(this).attr('stroke-width', '1px');
    })
    .on('mouseout', function () {
      d3.select(this).attr('stroke-width', '0.1px');
    })
    .append('title')
    .text(d => d + ': ' + result.get(d) + '%');

  svg.append('text')
    .attr('transform', 'translate(-6,' + cellHeight * 3.5 + ')rotate(-90)')
    .attr('text-anchor', 'middle')
    .text(() => {
      const y1 = startDate.getFullYear();
      const y2 = endDate.getFullYear();
      return y1 === y2 ? `${y1}` : `${y1} - ${y2}`;
    })
    .attr('class', 'heatmap-y-label');

  const months = svg.append('g')
    .selectAll('path')
    .data(monthRange)
    .enter();

  months
    .append('path')
    .attr('fill', 'none')
    .attr('stroke', '#000')
    .attr('stroke-width', '1.5px')
    .attr('d', function (startMonth) {
      if (startMonth < startDate) {
        startMonth.setDate(startDate.getDate());
      }
      const startWeekday = startMonth.getUTCDay();
      const startWeek = d3.timeMonday.count(startDate, startMonth);

      const endWeek = d3.timeMonday.count(startDate, endDate);
      const endWeekday = endDate.getUTCDay() - 1;

      return 'M' + (startWeek + 1) * cellWidth + ',' + startWeekday * cellHeight
        + 'H' + startWeek * cellWidth + 'V' + 7 * cellHeight
        + 'H' + endWeek * cellWidth + 'V' + (endWeekday + 1) * cellHeight
        + 'H' + (endWeek + 1) * cellWidth + 'V' + 0
        + 'H' + (startWeek + 1) * cellWidth + 'Z';
    });

  months
    .append('g')
    .attr(`transform`, (d) => `translate(${(d3.timeMonday.count(startDate, d) * cellWidth)}, ${height - 5})`)
    .append('text')
    .text(d => d.toLocaleString('nl', {month: "short"}))
    .attr('class', 'month-label');

}

function toStr(date: Date) {
  return date.getFullYear()
    + '-'
    + ('0' + (date.getMonth() + 1)).slice(-2)
    + '-'
    + ('0' + date.getDate()).slice(-2)
}
