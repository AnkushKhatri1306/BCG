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
  graphData: any;
  policyPageNumberSearch: number;
  graphYear: number;

  ngOnInit() {
    this.getInsurancePolicyData();
    this.getInsurancePolicyOptions();

  }

  // function to get data for the insurance plolicy and setting the data for displaying into the Html part
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

  // function for saving the insurance policy data 
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

    // function for getting the insurance policy options needed while editing the details
    getInsurancePolicyOptions(){
      this.policyService.getInsurancePolicyOptions().subscribe(resp => {
        if(resp.status == 'success'){
          this.policyOptions = resp.data;
          this.graphYear = this.policyOptions.graph_year_list[0];
          this.getInsurancePolicyGraph(this.graphYear);
          this.callToaster(resp.message, true);
        }
        else{
            this.callToaster(resp.message, false);
        }
      },
      error => {

      });
    }

    

    // function to get the detail of specific insurance policy detail 
    editInsurancePolicy(policyData: any){
      
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

    // function for setting the insurance policy page need to get for showing to the user
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


    // function for saving the insurance policy data 
    saveInsurancePolicy(){
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


    // function for getting the data need for making the chart and show into the Html page
    getInsurancePolicyGraph(year){
      
      this.policyService.getInsurancePolicyGraphData(year).subscribe(resp => {
        if(resp.status == 'success'){
          this.graphData = resp.data;
          this.callToaster(resp.message, true);
        }
        else{
            this.callToaster(resp.message, false);
        }
      },
      error => {

      });
             
    }


    // function for setting the toaster message and flag for showing error or success with timeout
    callToaster(message, successFlag){
      this.toasterMessage = message;
      this.successFlag = successFlag;
      this.showToaster = true;
      setTimeout(()=>{
        this.showToaster = false;
      }, 3000);
  }
}