import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { OperationComponent } from './operation/operation.component';
import { OperationListComponent } from './operation-list/operation-list.component';
import { OperationDetailComponent } from './operation-detail/operation-detail.component';

const routes: Routes = [
    {
        path: 'operations',
        component: OperationComponent,
        children: [
            {
                path: 'list',
                component: OperationListComponent
            },
            {
                path: 'detail',
                component: OperationDetailComponent
            }
        ]
    }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OperationRoutingModule { }
