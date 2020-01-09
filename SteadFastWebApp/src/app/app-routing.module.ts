import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { OperationFormComponent } from './pages/operation-form/operation-form.component';
import { OperationDetailComponent } from './operation/operation-detail/operation-detail.component';
import { PageNotFoundComponent } from './components/page-not-found/page-not-found.component';
import { OperationListComponent } from './operation/operation-list/operation-list.component';


const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'home', component: HomeComponent
  },
  {
    path: 'form', component: OperationFormComponent
  },
  {
    path: 'operations/list', component: OperationListComponent
  },
  {
    path: 'operations/:id', component: OperationDetailComponent
  },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
