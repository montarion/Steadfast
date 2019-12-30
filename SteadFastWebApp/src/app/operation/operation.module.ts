import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OperationComponent } from './operation/operation.component';
import { OperationListComponent } from './operation-list/operation-list.component';
import { OperationDetailComponent } from './operation-detail/operation-detail.component';
import { OperationRoutingModule } from './operation-routing.module';



@NgModule({
  declarations: [OperationComponent, OperationListComponent, OperationDetailComponent],
  imports: [
    CommonModule,
    OperationRoutingModule
  ]
})
export class OperationModule { }
