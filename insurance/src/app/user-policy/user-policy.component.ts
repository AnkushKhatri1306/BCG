import { Component, OnInit } from '@angular/core';
import { UserpolicyService } from '../_services/userpolicy.service';
declare var $: any;


@Component({
  selector: 'app-user-policy',
  templateUrl: './user-policy.component.html',
  styleUrls: ['./user-policy.component.css']
})
export class UserPolicyComponent implements OnInit {

  constructor(private policyService:UserpolicyService) { }

  policyDataList: any;
  getPolicyResponseData: any;
  openPopup: boolean = false; 
  policyDataParams: any;
  searchText: any = '';
  pageSize: number = 10;
  pageNumber: number = 1;
  policyData: any;
  policyPageNumberSearch: number;

  ngOnInit() {
    this.getInsurancePolicyData();

  }

  getInsurancePolicyData(){

    this.policyDataParams = {
      'page_size': this.pageSize,
      'page_number': this.pageNumber,
      'search_id': this.searchText 

    }

    this.policyService.getInsurancePolicyList(this.policyDataParams).subscribe(resp => {
      if(resp.status = 'success'){
        this.getPolicyResponseData = resp.data;
        this.policyDataList = resp.data.policy_data;
        // console.log(this.policyDataList);
        
      }
    },
    error => {

    });
  }

    saveInsurancePolicyData(){
      this.policyService.savePolicyData(this.policyData).subscribe(resp => {
        if(resp.status == 'success'){
          this.openPopup = false;
        }
      },
      error => {

      });
    }

    editInsurancePolicy(policyData: any){
      // hhere need to trigger popup and set the data for the popup 
      console.log(policyData);
      $("#showMoreModal").modal('show');
      this.policyData = policyData;
      
      
    }

    setInsurancePolicyPage(page){
      this.pageNumber = page;
      if(this.pageNumber < 1){
        this.pageNumber = 1
      }
      if(this.getPolicyResponseData.total_page && this.pageNumber > this.getPolicyResponseData.total_page){
        this.pageNumber = this.getPolicyResponseData.total_page;
      }
      this.getInsurancePolicyData();
    }

}