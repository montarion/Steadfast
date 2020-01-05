import { Component, OnInit, AfterViewInit, ElementRef } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, AfterViewInit {

  constructor(private elementRef: ElementRef) { }

  ngOnInit() {
  }

  ngAfterViewInit() {
    this.elementRef.nativeElement.ownerDocument.body.style.backgroundColor = '#343a40';
 }

}
