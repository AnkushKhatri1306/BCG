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
  showToaster: boolean = false; 
  successFlag: boolean = false; 
  policyDataParams: any;
  searchText: any = '';
  toasterMessage: any = '';
  pageSize: number = 10;
  pageNumber: number = 1;
  policyData: any;
  policyOptions: any;
  policyPageNumberSearch: number;

  ngOnInit() {
    this.getInsurancePolicyData();
    this.getInsurancePolicyOptions();

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
        this.callToaster(resp.message, true);
      }
      else{
          this.callToaster(resp.message, false);
      }
    },
    error => {

    });
  }

    saveInsurancePolicyData(){
      this.policyService.savePolicyData(this.policyData).subscribe(resp => {
        if(resp.status == 'success'){
          this.openPopup = false;
          this.callToaster(resp.message, true);
        }
        else{
            this.callToaster(resp.message, false);
        }
      },
      error => {

      });
    }

    getInsurancePolicyOptions(){
      this.policyService.getInsurancePolicyOptions().subscribe(resp => {
        if(resp.status == 'success'){
          this.policyOptions = resp.data;
          this.callToaster(resp.message, true);
        }
        else{
            this.callToaster(resp.message, false);
        }
      },
      error => {

      });
    }

    

    editInsurancePolicy(policyData: any){
      // hhere need to trigger popup and set the data for the popup 
      
      console.log(policyData); 
      this.policyService.getInsurancePolicy(policyData.id).subscribe(resp => {
        if(resp.status == 'success'){
          this.policyData = resp.data;
          this.openPopup = true;
          $("#showMoreModal").modal('show');     
          this.callToaster(resp.message, true);
        }
        else{
            this.callToaster(resp.message, false);
        }
      },
      error => {

      });
             
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

    saveInsurancePolicy(){
      console.log(this.policyData);
      this.policyService.savePolicyData(this.policyData).subscribe(resp => {
        if(resp.status == 'success'){
          $("#showMoreModal").modal('hide');  
          this.openPopup = false;
          this.getInsurancePolicyData();
          
          this.callToaster(resp.message, true);
        }
        else{
            this.callToaster(resp.message, false);
        }
      },
      error => {

      });
    }

    callToaster(message, successFlag){
      this.toasterMessage = message;
      this.successFlag = successFlag;
      this.showToaster = true;
      setTimeout(()=>{
        this.showToaster = false;
      }, 3000);
  }
}