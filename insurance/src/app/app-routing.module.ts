import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UserPolicyComponent } from './user-policy/user-policy.component';



const routes: Routes = [
  { path: 'user-policy', component: UserPolicyComponent },
  { path: '',  redirectTo: '/user-policy', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
