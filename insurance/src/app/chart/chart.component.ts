import { Component, OnInit } from '@angular/core';
import * as c3 from 'c3';  

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css'],
  inputs: ['chartData']
})
export class ChartComponent implements OnInit {
  public chartData: any;
  constructor() { }

  ngOnInit() {
  }

  ngAfterViewInit() {
      var chart = c3.generate({
        bindto: '#chart',
        data: {
          columns: this.chartData,
          type: 'bar'
        },
        bar: {
          width: {
            ratio: 0.5
          }
        },
        axis: {
          x: {
            type: 'category',
            categories: ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
          }
        }
      });
  }

}
