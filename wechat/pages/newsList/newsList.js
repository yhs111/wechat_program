// pages/newsList/newsList.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    barIndex: 0,
    search_string: "",
    barList: ["面包", "豆腐", "土豆", "茄子", "鸡翅", "菠菜", "馒头", "面条", "排骨"],
    newsList: [],
    searchList: [],
    search_type: false
  },
  enter(e){
    let string = e.detail.value
    if(!string){
      if(!this.data.search_type){
        wx.showToast({
          title: '搜索字段不能为空!',
          icon: "none",
          duration: 1500
        })
      }else{
        this.setData({
          search_type: true
        })
        wx.request({
          url: 'http://localhost:44313/main/getnewslist/' + this.data.barList[this.data.barIndex],
          success: res => {
            this.setData({
              newsList: res.data,
              search_string: ""
            })
          }
        })
        return
      }
    }
    wx.showLoading({
      title: '加载中',
    }),
    wx.request({
      url: 'http://localhost:44313/main/searchList?string=' + string,
      success: res=> {
        this.setData({
          newsList: res.data,
          search_type: true,
          search_string: string,
        })
        wx.hideLoading();
      }
    })
  },
  clickBar(e) {
    var index = e.currentTarget.dataset.index;
    this.setData({
      barIndex: index
    })
    wx.showLoading({
      title: '加载中',
    })
    let name = this.data.barList[index]
    wx.request({
      url: 'http://localhost:44313/main/getnewslist/' + name,
      success: res=>{
        this.setData({
          newsList: res.data
        })
        wx.hideLoading();
      }
    })
  },
  goDetail(e) {
    wx.showLoading({
      title: '正在跳转',
      duration: 1000
    })
    // console.log(e);
    wx.navigateTo({
      url: '../newsDetail/newsDetail?nid=' + e.currentTarget.dataset.nid,
    })
  }, 
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let name = options.type
    if(name){
      for (let i = 0; i < this.data.barList.length; i++) {
        if (this.data.barList[i] == name) {
          this.setData({
            barIndex: i
          })
          break
        }
      }
      // console.log(this.barIndex)
      // todo 待完善功能: 从详情页点击标签跳转到首页让上面的列表标签切换
    }
    wx.showLoading({
      title: '加载中',
    }),
    wx.request({
      url: 'http://localhost:44313/main/getnewslist/' + this.data.barList[this.data.barIndex],
      success: res => {
        this.setData({
          newsList: res.data
        })
        wx.hideLoading();
      }
    })
  },


  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})