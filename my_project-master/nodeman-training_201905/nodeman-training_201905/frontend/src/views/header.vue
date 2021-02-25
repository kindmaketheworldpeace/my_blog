<template>
    <div class="agent-header">
        <div class="bk-agent">
            <div class="bk-agent-logo">
                <img src="../images/logoIcon.png" alt="" />
                <p>{{$t('m.header.title')}}</p>
            </div>
            <div class="bk-agent-navbar">
                <ul>
                    <!-- <li v-for="nav in menuList">
                        <router-link 
                            :to="{name: nav.roleId}" 
                            :class="{'bk-click': nav.routerPath === '/' + nav.roleId || nav.routerPath === nav.roleId}">
                            {{$t(nav.name)}}
                        </router-link>
                    </li> -->
                    <!-- <li>
                        <a href="javascript:;" class="bk-none-click">{{$t('m.otherWord.router.node')}}</a>
                    </li> -->
                    <li>
                        <router-link 
                            :to="{name: 'stall'}" 
                            :class="{'bk-click': this.$route.path === '/'}"
                            @click.native="clickflash">
                            {{$t('m.otherWord.router.manag')}}
                        </router-link>
                    </li>
                    
                    <li>
                        <router-link 
                            :to="{name: 'plug'}" 
                            :class="{'bk-click': this.$route.path === '/plug'}"
                            @click.native="clickflash">
                            {{$t('m.otherWord.router.plug')}}
                        </router-link>
                    </li>
                    <li>
                        <router-link 
                            :to="{name: 'task'}" 
                            :class="{'bk-click': this.$route.path === '/task'}"
                            @click.native="clickflash">
                            {{$t('m.otherWord.router.task')}}
                        </router-link>
                    </li>
                    <!-- <li>
                        <a href="javascript:;" class="bk-none-click">{{$t('m.otherWord.router.healty')}}</a>
                    </li> -->
                </ul>
            </div>
            <div class="bk-agent-personal">
                <div class="bk-right">
                    <div class="bk-img">
                        <img src="../images/headimg.jpg" alt="" />
                    </div>
                    <div class="bk-word">
                        <span>{{headName}}</span>
                    </div>
                </div>
                <!-- <div class="bk-left bk-problem" style="padding-left: 0px">
                    <i class="bk-icon icon-more"></i>
                </div> -->
                <div class="bk-left bk-problem"
                    @click="showChange" 
                    :class="{'bk-import': showOpen && menuList.length}" 
                    v-if="showSuperuser"
                    style="padding: 0 20px;">
                    <i class="bk-icon icon-cog" style="color: #8393A8;"></i>
                    <!-- <span>Nginx Server</span> -->
                </div>
                <div class="bk-left bk-problem" 
                    @click="svgShow" 
                    :class="{'bk-import': showSvg && menuList.length}"
                    style="padding: 0 20px; margin-left: 10px">
                    <i class="bk-icon icon-question-circle" style="color: #8393A8;"></i>
                    <!-- <span>{{$t('m.header.schematic')}}</span> -->
                </div>
                <div class="bk-center">
                    <bk-selector 
                        :list="applications"
                        :setting-key="'ApplicationID'"
                        :display-key="'ApplicationName'"
                        :selected.sync="selectAppId"
                        @item-selected="getItem">
                    </bk-selector>
                </div>
            </div>
        </div>
        <div class="bk-open-change" v-if="showOpen && menuList.length"> 
            <!-- <div class="bk-stall-change">
                <div class="bk-ip-info">
                    <p class="bk-p-black">
                        {{$t('m.nginx.info.title')}}
                    </p>
                    <p class="bk-p-gray">
                        1. {{$t('m.nginx.info.pointOne')}}
                    </p>
                    <p class="bk-p-gray">
                        2. {{$t('m.nginx.info.pointTwo')}}
                    </p>
                </div>
                <div class="bk-splice-splice">
                    <div class="bk-change-ip">
                        <div class="bk-form-item bk-ip">
                            <label class="bk-label">{{$t('m.addNode.innerip')}}：</label>
                            <div class="bk-form-content">
                                <input 
                                    type="text" 
                                    class="bk-form-input"
                                    :class="{'bk-input-checked': verify.isIntra}"
                                    :placeholder="$t('m.addNode.please')" 
                                    v-model="inputIntra"
                                    @input="verifyInnerIp('inner')">
                            </div>
                        </div>
                        <div class="bk-form-item bk-ip ml55">
                            <label class="bk-label">{{$t('m.addNode.outerip')}}：</label>
                            <div class="bk-form-content">
                                <input 
                                    type="text" 
                                    class="bk-form-input" 
                                    :class="{'bk-input-checked': verify.isOuter}"
                                    :placeholder="$t('m.addNode.please')" 
                                    v-model="inputOuter"
                                    @input="verifyInnerIp('outer')">
                            </div>
                        </div>
                    </div>
                    <div class="bk-splice-line"></div>
                    <div class="bk-change-btn">
                        <button :class="['bk-button bk-primary', {'is-loading': isNginxSaving}]" @click="updataInfo('nginx')">{{$t('m.clickBtn.save')}}</button>
                    </div>
                </div> -->
                <!-- <div class="bk-ip-info" style="height: 100px;">
                    <p class="bk-p-black">
                        {{$t('m["安装Proxy时，需要从Nginx所在机器下载Linux、Windows、AIX所需要的agent安装包，约150 - 180 M大小"]')}}
                    </p>
                    <p class="bk-p-black">
                        {{$t('m["若Proxy到Nginx之间的网络带宽较小，容易超时。可以通过增大超时时间进行设置。"]')}}
                    </p>
                </div>
                <div class="bk-splice-splice" style="padding-bottom: 20px; border: none;">
                    <div class="bk-change-ip">
                        <div class="bk-form-item bk-ip">
                            <label class="bk-label" style="width: 83px;">{{$t('m.clickBtn.time')}}：</label>
                            <div class="bk-form-content">
                                <input 
                                    type="text" 
                                    class="bk-form-input"
                                    :class="{'bk-input-checked': verify.timeOut}"
                                    :placeholder="$t('m.clickBtn.timePlace')" 
                                    v-model="timeOut"
                                    @input="verifyInnerIp('time')">
                            </div>
                        </div>
                    </div>
                    <div class="bk-change-btn">
                        <button :class="['bk-button bk-primary', {'is-loading': isTimeSaving}]" @click="updataInfo('timeout')">{{$t('m.clickBtn.save')}}</button>
                    </div>
                </div>
                <div class="bk-ip-info" style="height: 64px;">
                    <p class="bk-p-black">
                        {{$t('m["请初始化插件信息，后台会读取中控机下的插件配置文件，如果没有初始化或者初始化失败，将无法使用插件管理相关功能"]')}}
                    </p>
                </div> -->
                <!-- <div class="bk-splice-splice" style="padding-bottom: 20px; border: none;">

                    <div class="bk-change-ip">
                        <div class="bk-form-item bk-ip">
                            <label class="bk-label" style="width: 272px;text-align: left;">{{$t('m["最后一次配置时间"]')}}：{{ configTime }}</label>
                        </div>
                    </div>

                    <div class="bk-change-btn">
                        <button :class="['bk-button bk-primary', {'is-loading': isPluginConfiging}]" @click="updatePlugin()">{{$t('m.clickBtn.configNow')}}</button>
                    </div>
                </div>
            </div> -->
            <nginx-server></nginx-server>

        </div>
        <!-- 配置Nginx Server -->
        <div class="bk-stall-ip">
            <div class="bk-content" v-if="openStatus">
                <p>
                    {{$t('m.nginx.welcome')}}
                </p>
                <div class="bk-btn">
                    <button class="bk-button bk-primary" @click="showChange">{{$t('m.nginx.configuration')}}</button>
                </div>
            </div> 
        </div>
        <!-- 遮罩层 -->
        <div class="bk-open-shade" v-if="showOpen"></div>
        <div class="bk-svg-shade" v-if="!showOpen && showSvg">
            <div class="bk-svg">
                <div class="bk-svg-img">
                    <svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xl="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 1029 586" width="1029" height="586">
                      <defs>
                        <font-face font-family="PingFang SC" font-size="16" panose-1="2 11 4 0 0 0 0 0 0 0" units-per-em="1000" underline-position="-150" underline-thickness="58" slope="0" x-height="600" cap-height="860" ascent="1060.0021" descent="-340.0007" font-weight="400">
                          <font-face-src>
                            <font-face-name name="PingFangSC-Regular"/>
                          </font-face-src>
                        </font-face>
                        <font-face font-family="Helvetica Neue" font-size="16" panose-1="2 0 5 3 0 0 0 2 0 4" units-per-em="1000" underline-position="-100" underline-thickness="50" slope="0" x-height="517" cap-height="714" ascent="951.9958" descent="-212.99744" font-weight="400">
                          <font-face-src>
                            <font-face-name name="HelveticaNeue"/>
                          </font-face-src>
                        </font-face>
                        <font-face font-family="Helvetica Neue" font-size="14" panose-1="2 0 5 3 0 0 0 2 0 4" units-per-em="1000" underline-position="-100" underline-thickness="50" slope="0" x-height="517" cap-height="714" ascent="951.9958" descent="-212.99744" font-weight="400">
                          <font-face-src>
                            <font-face-name name="HelveticaNeue"/>
                          </font-face-src>
                        </font-face>
                        <font-face font-family="Helvetica Neue" font-size="10" panose-1="2 0 5 3 0 0 0 2 0 4" units-per-em="1000" underline-position="-100" underline-thickness="50" slope="0" x-height="517" cap-height="714" ascent="951.9958" descent="-212.99744" font-weight="400">
                          <font-face-src>
                            <font-face-name name="HelveticaNeue"/>
                          </font-face-src>
                        </font-face>
                        <font-face font-family="Helvetica Neue" font-size="13" panose-1="2 0 5 3 0 0 0 2 0 4" units-per-em="1000" underline-position="-100" underline-thickness="50" slope="0" x-height="517" cap-height="714" ascent="951.9958" descent="-212.99744" font-weight="400">
                          <font-face-src>
                            <font-face-name name="HelveticaNeue"/>
                          </font-face-src>
                        </font-face>
                        <font-face font-family="Helvetica Neue" font-size="12" panose-1="2 0 5 3 0 0 0 2 0 4" units-per-em="1000" underline-position="-100" underline-thickness="50" slope="0" x-height="517" cap-height="714" ascent="951.9958" descent="-212.99744" font-weight="400">
                          <font-face-src>
                            <font-face-name name="HelveticaNeue"/>
                          </font-face-src>
                        </font-face>
                        <font-face font-family="PingFang SC" font-size="12" panose-1="2 11 4 0 0 0 0 0 0 0" units-per-em="1000" underline-position="-150" underline-thickness="58" slope="0" x-height="600" cap-height="860" ascent="1060.0021" descent="-340.0007" font-weight="400">
                          <font-face-src>
                            <font-face-name name="PingFangSC-Regular"/>
                          </font-face-src>
                        </font-face>
                      </defs>
                      <metadata> Produced by OmniGraffle 7.8 
                        <dc:date>2018-10-31 07:00:25 +0000</dc:date>
                      </metadata>
                      <g id="Canvas_1" fill-opacity="1" stroke-dasharray="none" stroke="none" stroke-opacity="1" fill="none">
                        <title>Canvas 1</title>
                        <rect fill="white" x="0" y="0" width="1029" height="586"/>
                        <g id="Canvas_1: Layer 1">
                          <title>Layer 1</title>
                          <g id="Group_2">
                            <title>Canvas_2</title>
                            <g id="Group_3">
                              <title>Canvas_2: {{$t('m["部署逻辑"]')}}</title>
                              <g id="Group_78">
                                <title>Graphic_61</title>
                                <g id="Graphic_80">
                                  <path d="M 240.92593 18.5 L 696 18.5 C 700.4183 18.5 704 22.081722 704 26.5 L 704 103.58481 C 704 108.00309 700.4183 111.58481 696 111.58481 L 240.92593 111.58481 C 236.50765 111.58481 232.92593 108.00309 232.92593 103.58481 L 232.92593 26.5 C 232.92593 22.081722 236.50765 18.5 240.92593 18.5 Z" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
                                </g>
                                <g id="Graphic_79">
                                  <title>Text</title>
                                  <text transform="translate(667 26)" fill="black">
                                    <tspan font-family="PingFang SC" font-size="16" font-weight="400" fill="black" x="0" y="17">{{$t('m["蓝鲸"]')}}</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_75">
                                <title>Graphic_60</title>
                                <g id="Graphic_77">
                                  <path d="M 436.28773 40.349096 L 516.47404 40.10959 C 520.4071 40.499045 524.0369 43.502134 524.0639 48.34827 M 524.06224 47.9478 L 524.19354 79.7841 C 523.8189 83.34703 520.1935 87.37578 516.0639 87.34827 M 516.2737 87.34871 L 436.2488 87.18104 C 431.9433 86.9133 428.40374 83.85323 428.5639 79.34827 M 428.5649 79.53678 L 428.4007 48.168903 C 428.56056 44.356695 431.93994 40.500294 436.5639 40.34827 M 436.3501 40.23649 L 516.0857 40.001945 C 520.5321 40.374045 524.1619 43.377134 524.1889 48.22327 M 524.1558 47.885174 L 524.27825 79.30104 C 523.9439 83.22203 520.3185 87.25078 516.1889 87.22327 M 516.3362 87.30792 L 436.5912 87.17129 C 432.0683 86.7883 428.52874 83.72823 428.6889 79.22327 M 428.61526 79.47435 L 428.4312 48.534314 C 428.68556 44.231695 432.06494 40.375294 436.6889 40.22327" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2.0,2.0" stroke-width="1"/>
                                </g>
                                <g id="Graphic_76">
                                  <title>Text</title>
                                  <text transform="translate(456.9059 55.40027)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="16" font-weight="400" fill="black" x=".092" y="15">nginx</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_72">
                                <title>Graphic_59</title>
                                <g id="Graphic_74">
                                  <path d="M 639.1093 269.00017 L 839.9628 268.91017 C 844.2715 268.60195 847.5657 272.4886 847.4836 277 M 847.4834 276.74954 L 847.659 573.1173 C 847.4676 577.3126 843.5328 580.9767 839.4836 581 M 839.8954 581.00045 L 639.2219 580.7827 C 634.8466 581.0633 631.2197 577.824 631.4836 573 M 631.48366 573.49864 L 631.4371 276.43507 C 631.40265 272.46232 634.93496 268.7173 639.4836 269 M 639.1718 268.91666 L 839.5701 268.81488 C 844.3965 268.47695 847.6907 272.3636 847.6086 276.875 M 847.5892 276.687 L 847.7218 572.84306 C 847.5926 577.1876 843.6578 580.8517 839.6086 580.875 M 839.9579 580.94825 L 639.42785 580.7487 C 634.9716 580.9383 631.3447 577.699 631.6086 572.875 M 631.5268 573.43614 L 631.4619 276.78953 C 631.52765 272.33732 635.05996 268.5923 639.6086 268.875" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2.0,2.0" stroke-width="1"/>
                                </g>
                                <g id="Graphic_73">
                                  <title>Text</title>
                                  <text transform="translate(778.4836 276.5)" fill="black">
                                    <tspan font-family="PingFang SC" font-size="16" font-weight="400" fill="black" x="0" y="17">{{$t('m.tabControl.directArea')}}</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_69">
                                <title>Graphic_58</title>
                                <g id="Graphic_71">
                                  <path d="M 150.52767 268.99986 L 351.5482 269.0582 C 355.35344 268.93548 359.19114 272.82336 359 277 M 358.99964 276.52455 L 359.22304 573.1738 C 359.2246 577.64244 355.8525 580.92594 351 581 M 351.2388 580.9997 L 150.41676 581.23285 C 146.34748 580.6983 142.63239 577.2594 143 573 M 142.9999 573.43376 L 143.06822 276.5495 C 142.83733 272.81225 146.52671 269.16624 151 269 M 151.33861 269 L 150.61226 269 M 150.59019 268.88295 L 351.1512 268.97608 C 355.47844 268.81048 359.31614 272.69836 359.125 276.875 M 359.1177 276.462 L 359.3246 572.7332 C 359.3496 577.51744 355.9775 580.80094 351.125 580.875 M 351.3014 580.9986 L 150.8612 581.1744 C 146.47248 580.5733 142.75739 577.1344 143.125 572.875 M 143.03584 573.37126 L 143.08932 276.89317 C 142.96233 272.68725 146.65171 269.04124 151.125 268.875 M 151.40111 268.94214 L 151.0625 268.95568" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
                                </g>
                                <g id="Graphic_70">
                                  <title>Text</title>
                                  <text transform="translate(148 276.5)" fill="black">
                                    <tspan font-family="PingFang SC" font-size="16" font-weight="400" fill="black" x=".052" y="17">{{$t('m["云区域"]')}}</tspan>
                                    <tspan font-family="Helvetica Neue" font-size="16" font-weight="400" fill="black" y="17">1</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_66">
                                <title>Graphic_57</title>
                                <g id="Graphic_68">
                                  <path d="M 176.8046 343.53096 L 314.61724 343.73773 C 318.78526 343.7907 322.3002 346.8057 322 351.53125 M 322.00196 351.2058 L 321.76915 389.8865 C 321.57873 393.6116 318.77213 397.4064 314 397.53125 M 314.4408 397.53066 L 176.97017 397.7135 C 172.30285 397.728 169.4123 394.10965 169 389.53125 M 168.99822 389.90014 L 169.18458 351.1952 C 168.75163 346.8143 172.60204 343.26277 177 343.53125 M 176.86712 343.44314 L 314.2158 343.66853 C 318.91026 343.6657 322.4252 346.6807 322.125 351.40625 M 322.06977 351.14335 L 321.84847 389.6548 C 321.70373 393.4866 318.89713 397.2814 314.125 397.40625 M 314.50338 397.51814 L 177.27813 397.69386 C 172.42785 397.603 169.5373 393.98465 169.125 389.40625 M 169.02694 389.83747 L 169.20033 351.5279 C 168.87663 346.6893 172.72704 343.13777 177.125 343.40625" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2.0,2.0" stroke-width="1"/>
                                </g>
                                <g id="Graphic_67">
                                  <title>Text</title>
                                  <text transform="translate(276.12 349.30725)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="16" font-weight="400" fill="black" x=".06" y="15">Proxy</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_63">
                                <title>Graphic_56</title>
                                <g id="Graphic_65">
                                  <path d="M 738.2065 328.90695 L 807.1863 328.7588 C 810.8631 328.63915 814.9092 332.51552 814.5 336.9063 M 814.50265 336.7309 L 814.3125 349.31804 C 814.2944 353.29034 811.1917 356.7307 806.5 356.9063 M 806.7678 356.9058 L 738.1486 357.0387 C 733.7867 356.7073 730.8086 352.9201 730.5 348.9063 M 730.5052 349.2103 L 730.2906 336.68477 C 730.1622 332.5523 734.1774 329.0868 738.5 328.90632 M 738.2689 328.78573 L 806.7803 328.6423 C 810.9881 328.51415 815.0342 332.39052 814.625 336.7813 M 814.5827 336.6687 L 814.4348 348.9208 C 814.4194 353.16534 811.3167 356.6057 806.625 356.7813 M 806.8304 356.88186 L 738.695 356.99464 C 733.9117 356.5823 730.9336 352.7951 730.625 348.7813 M 730.5267 349.1485 L 730.3114 337.00765 C 730.2872 332.4273 734.3024 328.9618 738.625 328.78132" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
                                </g>
                                <g id="Graphic_64">
                                  <title>Text</title>
                                  <text transform="translate(774.234 334.46032)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="14" font-weight="400" fill="black" x=".367" y="13">agent</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_61">
                                <title>Graphic_55</title>
                                <g id="Graphic_62">
                                  <path d="M 738.1084 377.4063 L 806.7553 377.4075 C 811.3252 377.4624 814.1346 381.35027 814.5 385.4063 M 814.5045 385.00594 L 814.3636 397.49955 C 814.5212 402.10946 811.1114 405.1799 806.5 405.4063 M 806.9698 405.40576 L 738.202 405.4877 C 733.7713 405.7198 730.70485 401.73913 730.5 397.4063 M 730.5017 397.64546 L 730.4091 384.79917 C 730.1153 381.3843 734.2527 377.15206 738.5 377.4063 M 738.1709 377.3142 L 806.345 377.3035 C 811.4502 377.3374 814.2596 381.22527 814.625 385.2813 M 814.5968 384.9438 L 814.4587 397.3105 C 814.6462 401.98446 811.2364 405.0549 806.625 405.2813 M 807.0323 405.3704 L 738.6119 405.48283 C 733.8963 405.5948 730.82985 401.61413 730.625 397.2813 M 730.516 397.5833 L 730.4224 385.11086 C 730.2403 381.2593 734.3777 377.02706 738.625 377.2813" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2.0,2.0" stroke-width="1"/>
                                </g>
                              </g>
                              <g id="Group_59">
                                <title>Graphic_54</title>
                                <g id="Graphic_60">
                                  <path d="M 738.0103 425.90525 L 806.8243 426.05626 C 810.8666 426.30773 814.2437 429.30136 814.5 433.9063 M 814.50185 433.65593 L 814.4103 446.05603 C 814.7593 450.03167 811.031 453.62913 806.5 453.9063 M 806.7968 453.9062 L 738.2554 453.93693 C 733.7566 453.83623 730.6011 450.55817 730.5 445.9063 M 730.4996 446.0806 L 730.5271 433.4136 C 730.8854 429.38224 734.328 426.101 738.5 425.9063 M 738.0728 425.8422 L 806.4096 425.9647 C 810.9916 426.18273 814.3687 429.17636 814.625 433.7813 M 814.6064 433.59375 L 814.4826 445.7004 C 814.8843 449.90667 811.156 453.50413 806.625 453.7813 M 806.8593 453.8594 L 738.5287 453.90853 C 733.8816 453.71123 730.7261 450.43317 730.625 445.7813 M 730.5067 446.01797 L 730.5334 433.714 C 731.0104 429.25724 734.453 425.976 738.625 425.7813" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2.0,2.0" stroke-width="1"/>
                                </g>
                              </g>
                              <g id="Group_57">
                                <title>Graphic_53</title>
                                <g id="Graphic_58">
                                  <path d="M 738.2873 473.15696 L 806.8934 472.9515 C 811.3226 472.99136 814.3527 476.8861 814.5 481.1563 M 814.5016 480.68094 L 814.4583 493.8625 C 814.12 497.60646 810.9506 500.82835 806.5 501.1563 M 806.9988 501.15647 L 737.9338 501.13623 C 733.7427 501.57734 730.4974 497.24354 730.5 493.1563 M 730.4943 493.6407 L 730.645 480.77807 C 730.8148 476.9841 734.4034 472.9163 738.5 473.1563 M 738.34965 473.0605 L 806.4741 472.8759 C 811.4476 472.86636 814.4777 476.7611 814.625 481.0313 M 814.6184 480.6186 L 814.5689 493.3407 C 814.245 497.48146 811.0756 500.70335 806.625 501.0313 M 807.0613 501.0983 L 738.4456 501.08423 C 733.8677 501.45234 730.6224 497.11854 730.625 493.0313 M 730.55665 493.5782 L 730.6444 481.0671 C 730.9398 476.8591 734.5284 472.7913 738.625 473.0313" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2.0,2.0" stroke-width="1"/>
                                </g>
                              </g>
                              <g id="Group_54">
                                <title>Graphic_52</title>
                                <g id="Graphic_56">
                                  <path d="M 287.50306 40.348466 L 377.5263 40.29227 C 381.4402 40.52196 385.02567 43.52915 385.0639 48.34827 M 385.0638 48.0229 L 385.0712 79.73595 C 384.8969 84.10682 381.4341 86.96952 377.0639 87.34827 M 377.38967 87.34853 L 287.30112 87.27759 C 283.04335 87.39781 279.70755 83.75453 279.8139 79.34827 M 279.8172 79.76778 L 279.56662 48.08444 C 280.0543 43.644727 283.7926 40.557166 287.8139 40.34827 M 287.56556 40.28112 L 377.10266 40.229067 C 381.5652 40.39696 385.15067 43.40415 385.1889 48.22327 M 385.1304 47.9604 L 385.1567 79.42267 C 385.0219 83.98182 381.5591 86.84452 377.1889 87.22327 M 377.45213 87.34144 L 287.67634 87.26438 C 283.16835 87.27281 279.83255 83.62953 279.9389 79.22327 M 279.8723 79.705335 L 279.6318 48.363414 C 280.1793 43.519727 283.9176 40.432166 287.9389 40.22327" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2.0,2.0" stroke-width="1"/>
                                </g>
                                <g id="Graphic_55">
                                  <title>Text</title>
                                  <text transform="translate(300.37776 43.34853)" fill="black">
                                    <tspan font-family="PingFang SC" font-size="16" font-weight="400" fill="black" x="10.336" y="17">APPO</tspan>
                                    <tspan font-family="PingFang SC" font-size="16" font-weight="400" fill="black" x="0" y="39">{{$t('m.header.title')}}</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_52">
                                <title>Graphic_51</title>
                                <g id="Graphic_53">
                                  <title>Text</title>
                                  <text transform="translate(884 478.6563)" fill="black">
                                    <tspan font-family="PingFang SC" font-size="16" font-weight="400" fill="black" x="0" y="17">{{$t('m["受控主机"]')}}</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_50">
                                <title>Line_50</title>
                                <g id="Line_51">
                                  <line x1="329.39346" y1="86.8565" x2="260.6743" y2="343.53125" stroke="#797ed6" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                                </g>
                              </g>
                              <g id="Group_47">
                                <title>Graphic_49</title>
                                <g id="Graphic_49">
                                  <rect x="279.81446" y="203.51343" width="30" height="25" fill="white"/>
                                </g>
                                <g id="Graphic_48">
                                  <title>Text</title>
                                  <text transform="translate(284.89446 210.62343)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="10" font-weight="400" fill="black" x=".41" y="10">SSH</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_45">
                                <title>Line_48</title>
                                <g id="Line_46">
                                  <line x1="513.83175" y1="86.92863" x2="758.35285" y2="328.90632" stroke="#ff2841" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                                </g>
                              </g>
                              <g id="Group_43">
                                <title>Line_47</title>
                                <g id="Line_44">
                                  <line x1="448.79004" y1="87.34827" x2="299.0791" y2="343.53125" stroke="#ff2841" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                                </g>
                              </g>
                              <g id="Group_40">
                                <title>Graphic_46</title>
                                <g id="Graphic_42">
                                  <path d="M 240.7766 429.69167 L 314.00156 429.52153 C 318.4004 430.1156 321.7324 433.11337 322 437.6913 M 322.00305 437.51606 L 321.7831 450.1678 C 322.32653 453.71184 318.7716 457.8915 314 457.6913 M 314.41274 457.6906 L 240.48363 457.81847 C 236.88112 458.09203 233.08086 454.24446 232.92593 449.6913 M 232.9279 450.0966 L 232.86732 437.61413 C 232.6672 433.36813 236.47295 429.94287 240.92593 429.6913 M 240.83906 429.6114 L 313.92626 429.41433 C 318.5254 429.9906 321.8574 432.98837 322.125 437.5663 M 322.08065 437.4538 L 321.86104 449.607 C 322.45153 453.58684 318.8966 457.7665 314.125 457.5663 M 314.47533 457.67753 L 240.78977 457.7866 C 237.00612 457.96703 233.20586 454.11946 233.05093 449.5663 M 232.93966 450.03433 L 232.90994 437.82853 C 232.7922 433.24313 236.59795 429.81787 241.05093 429.5663" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
                                </g>
                                <g id="Graphic_41">
                                  <title>Text</title>
                                  <text transform="translate(277.753 435.0093)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="13" font-weight="400" fill="black" x=".2435" y="12">p-agent</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_38">
                                <title>Graphic_45</title>
                                <g id="Graphic_39">
                                  <path d="M 240.67852 472.1914 L 314.0706 472.1695 C 318.8538 472.0511 321.84146 475.9481 322 480.1913 M 322.00542 479.7911 L 321.83527 492.34935 C 321.66097 496.5293 318.69122 500.34074 314 500.1913 M 314.23974 500.19107 L 240.66205 500.2681 C 236.89622 500.23206 232.97713 496.17984 232.92593 492.1913 M 232.92433 492.5317 L 232.98446 479.7286 C 232.61242 475.3561 236.54828 472.00815 240.92593 472.1913 M 240.741 472.0777 L 313.99096 472.07554 C 318.9788 471.9261 321.96646 475.8231 322.125 480.0663 M 322.09528 479.72895 L 321.9474 491.9977 C 321.78597 496.4043 318.81622 500.21574 314.125 500.0663 M 314.30228 500.1666 L 241.2066 500.2123 C 237.02122 500.10706 233.10213 496.05484 233.05093 492.0663 M 232.92887 492.46894 L 233.02095 479.93197 C 232.73742 475.2311 236.67328 471.88315 241.05093 472.0663" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2.0,2.0" stroke-width="1"/>
                                </g>
                              </g>
                              <g id="Group_36">
                                <title>Graphic_44</title>
                                <g id="Graphic_37">
                                  <path d="M 240.58044 514.6907 L 314.13962 514.8175 C 318.40906 514.888 321.9505 517.8992 322 522.6913 M 322.0024 522.4411 L 321.8822 534.9058 C 321.89565 539.3622 318.61084 542.78996 314 542.6913 M 314.44173 542.69116 L 240.71546 542.7172 C 236.86794 542.3391 232.8734 538.9989 232.92593 534.6913 M 232.922 534.9668 L 233.1014 522.34304 C 232.52556 518.1947 236.6236 514.9571 240.92593 514.6913 M 240.64297 514.60614 L 314.0556 514.73674 C 318.53406 514.763 322.0755 517.7742 322.125 522.5663 M 322.10452 522.37895 L 321.97128 534.3875 C 322.02065 539.2372 318.73584 542.66496 314.125 542.5663 M 314.50424 542.6553 L 241.1235 542.7005 C 236.99294 542.2141 232.9984 538.8739 233.05093 534.5663 M 232.98183 534.9043 L 233.13197 522.53534 C 232.65056 518.0697 236.7486 514.8321 241.05093 514.5663" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2.0,2.0" stroke-width="1"/>
                                </g>
                              </g>
                              <g id="Group_34">
                                <title>Line_43</title>
                                <g id="Graphic_35">
                                  <path d="M 191.32245 397.1518 L 191.32245 404.1518 L 191.32245 441.21426 C 191.32245 442.31883 192.21788 443.21426 193.32245 443.21426 L 227.10466 443.21426 C 227.112 443.21426 227.11933 443.2143 227.12667 443.2144 L 232.92593 443.2782" stroke="#3ca600" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
                                </g>
                              </g>
                              <g id="Group_32">
                                <title>Line_42</title>
                                <g id="Graphic_33">
                                  <path d="M 191.32245 397.1518 L 191.32245 404.1518 L 191.32245 483.3299 C 191.32245 484.4345 192.21788 485.3299 193.32245 485.3299 L 229.98922 485.3299 L 232.92593 485.3299" stroke="#3ca600" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
                                </g>
                              </g>
                              <g id="Group_30">
                                <title>Line_41</title>
                                <g id="Graphic_31">
                                  <path d="M 191.32245 397.1518 L 191.32245 404.1518 L 191.32245 525.98886 C 191.32245 527.0934 192.21788 527.98886 193.32245 527.98886 L 230.90068 527.98886 L 232.92593 527.98886" stroke="#3ca600" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
                                </g>
                              </g>
                              <g id="Group_27">
                                <title>Graphic_40</title>
                                <g id="Graphic_29">
                                  <rect x="582" y="196.5667" width="30" height="25" fill="white"/>
                                </g>
                                <g id="Graphic_28">
                                  <title>Text</title>
                                  <text transform="translate(587.08 203.6767)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="10" font-weight="400" fill="black" x=".41" y="10">SSH</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_24">
                                <title>Graphic_39</title>
                                <g id="Graphic_26">
                                  <rect x="616.7445" y="194.08373" width="36" height="25" fill="white"/>
                                </g>
                                <g id="Graphic_25">
                                  <title>Text</title>
                                  <text transform="translate(621.7445 201.19373)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="10" font-weight="400" fill="black" x=".41" y="10">HTTP</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_22">
                                <title>Line_38</title>
                                <g id="Graphic_23">
                                  <path d="M 3712322 974.8126 L 3567753 974.8126 L 3443985.8 974.8126" stroke="black" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
                                </g>
                              </g>
                              <g id="Group_20">
                                <title>Graphic_37</title>
                                <g id="Graphic_21">
                                  <title>Text</title>
                                  <text transform="translate(391.75 520.1913)" fill="black">
                                    <tspan font-family="PingFang SC" font-size="16" font-weight="400" fill="black" x="0" y="17">{{$t('m["受控主机"]')}}</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_18">
                                <title>Line_36</title>
                                <g id="Graphic_19">
                                  <path d="M 1644773.7 1057.8826 L 1493239.8 1057.8826 L 1373305.3 1057.8826" stroke="black" stroke-linecap="round" stroke-linejoin="round" stroke-width="1"/>
                                </g>
                              </g>
                              <g id="Group_15">
                                <title>Graphic_35</title>
                                <g id="Graphic_17">
                                  <rect x="360.04007" y="195.91452" width="36" height="25" fill="white"/>
                                </g>
                                <g id="Graphic_16">
                                  <title>Text</title>
                                  <text transform="translate(365.04007 203.02452)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="10" font-weight="400" fill="black" x=".41" y="10">HTTP</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_13">
                                <title>Graphic_34</title>
                                <g id="Graphic_14">
                                  <title>Text</title>
                                  <text transform="translate(713.438 145.25)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="12" font-weight="400" fill="black" x=".164" y="13">HTTP </tspan>
                                    <tspan font-family="PingFang SC" font-size="12" font-weight="400" fill="black" y="13">{{$t('m["请求"]')}}</tspan>
                                    <tspan font-family="Helvetica Neue" font-size="12" font-weight="400" fill="black" y="13">: </tspan>
                                    <tspan font-family="PingFang SC" font-size="12" font-weight="400" fill="black" y="13">{{$t('m["从"]')}}</tspan>
                                    <tspan font-family="Helvetica Neue" font-size="12" font-weight="400" fill="black" y="13"> Nginx </tspan>
                                    <tspan font-family="PingFang SC" font-size="12" font-weight="400" fill="black" y="13">{{$t('m["机器下载安装脚本"]')}}</tspan>
                                    <tspan font-family="Helvetica Neue" font-size="12" font-weight="400" fill="black" y="13">, </tspan>
                                    <tspan font-family="PingFang SC" font-size="12" font-weight="400" fill="black" y="13">{{$t('m["以及安装包"]')}}</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_11">
                                <title>Graphic_33</title>
                                <g id="Graphic_12">
                                  <title>Text</title>
                                  <text transform="translate(712.606 166.56883)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="12" font-weight="400" fill="black" x=".496" y="13">SSH </tspan>
                                    <tspan font-family="PingFang SC" font-size="12" font-weight="400" fill="black" y="13">{{$t('m["请求"]')}}</tspan>
                                    <tspan font-family="Helvetica Neue" font-size="12" font-weight="400" fill="black" y="13">: SaaS </tspan>
                                    <tspan font-family="PingFang SC" font-size="12" font-weight="400" fill="black" y="13">{{$t('m["应用从"]')}}</tspan>
                                    <tspan font-family="Helvetica Neue" font-size="12" font-weight="400" fill="black" y="13"> APPO </tspan>
                                    <tspan font-family="PingFang SC" font-size="12" font-weight="400" fill="black" y="13">{{$t('m["机器"]')}}</tspan>
                                    <tspan font-family="Helvetica Neue" font-size="12" font-weight="400" fill="black" y="13"> SSH </tspan>
                                    <tspan font-family="PingFang SC" font-size="12" font-weight="400" fill="black" y="13">{{$t('m["登陆到目标机器"]')}}</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_9">
                                <title>Line_32</title>
                                <g id="Line_10">
                                  <line x1="369.49726" y1="87.34827" x2="750.4227" y2="328.90632" stroke="#797ed6" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                                </g>
                              </g>
                              <g id="Group_6">
                                <title>Graphic_31</title>
                                <g id="Graphic_8">
                                  <path d="M 560.5044 40.348015 L 650.287 40.39448 C 654.2551 40.4771 657.85084 43.489606 658.25 48.34827 M 658.25 48.173174 L 658.2531 79.54707 C 658.50054 83.71204 654.69956 87.6704 650.25 87.34827 M 650.69265 87.34892 L 560.6089 87.21726 C 556.664 87.36113 553.3663 83.38498 553 79.34827 M 552.99906 79.53042 L 553.1635 47.612716 C 553.29414 44.05717 556.7933 40.264627 561 40.34827 M 560.56694 40.266664 L 650.1454 40.301825 C 654.3801 40.3521 657.97584 43.364606 658.375 48.22327 M 658.3239 48.110673 L 658.3441 79.116695 C 658.62554 83.58704 654.82456 87.5454 650.375 87.22327 M 650.75515 87.28965 L 561.11696 87.20404 C 556.789 87.23613 553.4913 83.25998 553.125 79.22327 M 553.0275 79.46775 L 553.21176 48.040213 C 553.41914 43.93217 556.9183 40.139627 561.125 40.22327" stroke="#4180ff" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2.0,2.0" stroke-width="1"/>
                                </g>
                                <g id="Graphic_7">
                                  <title>Text</title>
                                  <text transform="translate(578.825 43.84827)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="16" font-weight="400" fill="black" x="5.632" y="17">GSE </tspan>
                                    <tspan font-family="PingFang SC" font-size="16" font-weight="400" fill="black" y="17">{{$t('m["等"]')}}</tspan>
                                    <tspan font-family="PingFang SC" font-size="16" font-weight="400" fill="black" x="0" y="39">{{$t('m["其他服务"]')}}</tspan>
                                  </text>
                                </g>
                              </g>
                              <g id="Group_4">
                                <title>Graphic_30</title>
                                <g id="Graphic_5">
                                  <title>Text</title>
                                  <text transform="translate(714.616 91.33481)" fill="black">
                                    <tspan font-family="Helvetica Neue" font-size="12" font-weight="400" fill="black" x=".432" y="13">APPO: </tspan>
                                    <tspan font-family="PingFang SC" font-size="12" font-weight="400" fill="black" y="13">{{$t('m["运行节点管理"]')}}</tspan>
                                    <tspan font-family="Helvetica Neue" font-size="12" font-weight="400" fill="black" y="13"> App </tspan>
                                    <tspan font-family="PingFang SC" font-size="12" font-weight="400" fill="black" y="13">{{$t('m["所在的机器"]')}}</tspan>
                                    <tspan font-family="Helvetica Neue" font-size="12" font-weight="400" fill="black" y="13">.</tspan>
                                  </text>
                                </g>
                              </g>
                            </g>
                          </g>
                        </g>
                      </g>
                    </svg>
                </div>
                <div class="bk-svg-info">
                    <div class="bj-svg-step">
                        <p class="bk-p-black">
                            {{$t('m.otherWord.figure.agentInstall')}}
                        </p>
                        <p class="bk-p-black bk-indent">
                            <span class="bk-round">·</span> {{$t('m.otherWord.figure.direaAgent')}}:
                        </p>
                        <p class="bk-p-gray">
                            1. {{$t('m.otherWord.figure.appoAgent')}}
                        </p>
                        <p class="bk-p-black bk-black-ml bk-indent">
                            <span class="bk-round">·</span> {{$t('m.otherWord.figure.noAgent')}}:
                        </p>
                        <p class="bk-p-gray">
                            1. {{$t('m.otherWord.figure.appoProxy')}}.
                        </p>
                        <p class="bk-p-gray">
                            2. {{$t('m.otherWord.figure.job')}}
                        </p>
                    </div>
                    <hr>
                    <div class="bj-svg-table">
                        <p class="bk-p-black">
                            {{$t('m.otherWord.figure.net')}}
                        </p>
                        <p class="bk-p-black bk-indent">
                            <span class="bk-round">·</span> {{$t('m.otherWord.figure.agentPort')}}。
                        </p>
                        <p class="bk-p-black bk-indent">
                            <span class="bk-round">·</span> {{$t('m.otherWord.figure.ssh')}}
                        </p>
                        <div class="bk-tab-svg">
                            <div class="bk-tab-change">
                                <ul>
                                    <li v-for="(item, index) in navbar" :class="{'bk-bord': index === indexNum, 
                                    'bk-splice': index === 2}" @click="changeNavbar(item, index)">
                                        <span>{{item.name}}</span>
                                    </li>
                                </ul>
                            </div>
                            <table class="bk-table has-table-bordered has-table-hover">
                                <thead>
                                    <tr>
                                        <th>{{$t('m.addSomeInfo.source')}}</th>
                                        <th>{{$t('m.addSomeInfo.target')}}</th>
                                        <th style="text-align: center;">{{$t('m.addSomeInfo.protocol')}}</th>
                                        <th>{{$t('m.addSomeInfo.port')}}</th>
                                        <th>{{$t('m.addSomeInfo.usage')}}</th>
                                        <th>{{$t('m.addSomeInfo.remark')}}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="item in tableInfo">
                                        <td>{{item.port}}</td>
                                        <td>{{item.type}}</td>
                                        <td style="text-align: center;">{{item.adress}}</td>
                                        <td>{{item.name}}</td>
                                        <td>{{item.msg}}</td>
                                        <td>{{item.osSame}}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import ajax from '../utils/ajax'
    import cookie from 'cookie'
    import nginxServer from './common/nginxServer.vue'

    export default {
        components: {
            nginxServer
        },
        data () {
            return {
                showSuperuser: '',
                selectAppId: 2,
                headName: '',
                configTime: '',
                // 输入框双向数据
                inputIntra: '',
                inputOuter: '',
                timeOut: '',
                gseInnerIp: '',
                gseOuterIp: '',
                // 按钮保存loading状态
                isNginxSaving: false,
                isPluginConfiging: false,
                isTimeSaving: false,
                showSvg: false,
                showOpen: false,
                // 验证判定型值
                verify: {
                    isIntra: false,
                    isOuter: false,
                    timeOut: false
                },
                indexNum: 0,
                navbar: [
                    {id: 0, name: this.$t('m.addSomeInfo.direct')},
                    {id: 1, name: this.$t('m.addSomeInfo.agentGse')},
                    {id: 2, name: this.$t('m.addSomeInfo.pagentGse')}
                ],
                // 表格信息
                tableInfo: [
                    {port: 'agent', type: 'zk', name: 'TCP', adress: '2181', msg: this.$t('m.addSomeInfo.query'), osSame: ''},
                    {port: 'agent', type: 'gse_task', name: 'TCP', adress: '48533', msg: this.$t('m.addSomeInfo.task'), osSame: ''},
                    {port: 'agent', type: 'gse_data', name: 'TCP', adress: '58625', msg: this.$t('m.addSomeInfo.data'), osSame: ''},
                    {port: 'agent', type: 'gse_btsvr', name: 'TCP', adress: '59173', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'agent', type: 'gse_btsvr', name: 'TCP,UDP', adress: '10020', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'agent', type: 'gse_btsvr', name: 'UDP', adress: '10030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'gse_btsvr', type: 'agent', name: 'TCP,UDP', adress: '60020-60030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'gse_btsvr', type: 'gse_btsvr', name: 'TCP', adress: '58930', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'gse_btsvr', type: 'gse_btsvr', name: 'TCP,UDP', adress: '10020', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'gse_btsvr', type: 'gse_btsvr', name: 'UDP', adress: '10030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'agent', type: 'agent', name: 'TCP,UDP', adress: '60020-60030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'agent', type: '', name: '', adress: this.$t('m.addSomeInfo.random'), msg: this.$t('m.addSomeInfo.btNone'), osSame: ''},
                    {port: 'gse_btsvr', type: '', name: '', adress: this.$t('m.addSomeInfo.random'), msg: this.$t('m.addSomeInfo.btNone'), osSame: ''}
                ],
                agentGse: [
                    {port: 'agent', type: 'zk', name: 'TCP', adress: '2181', msg: this.$t('m.addSomeInfo.query'), osSame: ''},
                    {port: 'agent', type: 'gse_task', name: 'TCP', adress: '48533', msg: this.$t('m.addSomeInfo.task'), osSame: ''},
                    {port: 'agent', type: 'gse_data', name: 'TCP', adress: '58625', msg: this.$t('m.addSomeInfo.data'), osSame: ''},
                    {port: 'agent', type: 'gse_btsvr', name: 'TCP', adress: '59173', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'agent', type: 'gse_btsvr', name: 'TCP,UDP', adress: '10020', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'agent', type: 'gse_btsvr', name: 'UDP', adress: '10030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'gse_btsvr', type: 'agent', name: 'TCP,UDP', adress: '60020-60030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'gse_btsvr', type: 'gse_btsvr', name: 'TCP', adress: '58930', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'gse_btsvr', type: 'gse_btsvr', name: 'TCP,UDP', adress: '10020', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'gse_btsvr', type: 'gse_btsvr', name: 'UDP', adress: '10030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'agent', type: 'agent', name: 'TCP,UDP', adress: '60020-60030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'agent', type: '', name: '', adress: this.$t('m.addSomeInfo.random'), msg: this.$t('m.addSomeInfo.btNone'), osSame: ''},
                    {port: 'gse_btsvr', type: '', name: '', adress: this.$t('m.addSomeInfo.random'), msg: this.$t('m.addSomeInfo.btNone'), osSame: ''}
                ],
                proxyGse: [
                    {port: 'proxy(gse_agent)', type: 'gse_task', name: 'TCP', adress: '48533', msg: this.$t('m.addSomeInfo.task'), osSame: ''},
                    {port: 'proxy(gse_transit)', type: 'gse_data', name: 'TCP', adress: '58625', msg: this.$t('m.addSomeInfo.data'), osSame: ''},
                    {port: 'proxy(gse_btsvr)', type: 'gse_btsvr', name: 'TCP', adress: '58930', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'proxy(gse_btsvr)', type: 'gse_btsvr', name: 'TCP,UDP', adress: '10020', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'proxy(gse_btsvr)', type: 'gse_btsvr', name: 'UDP', adress: '10030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'gse_btsvr', type: 'proxy(gse_btsvr)', name: 'TCP', adress: '58930', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'gse_btsvr', type: 'proxy(gse_btsvr)', name: 'TCP,UDP', adress: '10020', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'gse_btsvr', type: 'proxy(gse_btsvr)', name: 'UDP', adress: '10030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'proxy(gse_btsvr)', type: 'proxy(gse_btsvr)', name: 'TCP', adress: '58930', msg: this.$t('m.addSomeInfo.bt'), osSame: this.$t('m.addSomeInfo.same')},
                    {port: 'proxy(gse_btsvr)', type: 'proxy(gse_btsvr)', name: 'TCP,UDP', adress: '10020', msg: this.$t('m.addSomeInfo.bt'), osSame: this.$t('m.addSomeInfo.same')},
                    {port: 'proxy(gse_btsvr)', type: 'proxy(gse_btsvr)', name: 'UDP', adress: '10030', msg: this.$t('m.addSomeInfo.bt'), osSame: this.$t('m.addSomeInfo.same')},
                    {port: 'proxy(gse_opts)', type: 'gse_ops', name: 'TCP', adress: '58725', msg: this.$t('m.addSomeInfo.ping'), osSame: ''},
                    {port: 'proxy(gse_agent)', type: '', name: '', adress: this.$t('m.addSomeInfo.random'), msg: this.$t('m.addSomeInfo.btNone'), osSame: ''},
                    {port: 'proxy(gse_btsvr)', type: '', name: '', adress: this.$t('m.addSomeInfo.random'), msg: this.$t('m.addSomeInfo.btNone'), osSame: ''}
                ],
                pagentGse: [
                    {port: 'agent', type: 'proxy(gse_agent)', name: 'TCP', adress: '48533', msg: this.$t('m.addSomeInfo.task'), osSame: ''},
                    {port: 'agent', type: 'proxy(gse_transit)', name: 'TCP', adress: '58625', msg: this.$t('m.addSomeInfo.data'), osSame: ''},
                    {port: 'agent', type: 'proxy(gse_btsvr)', name: 'TCP', adress: '59173', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'agent', type: 'proxy(gse_btsvr)', name: 'TCP,UDP', adress: '10020', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'agent', type: 'proxy(gse_btsvr)', name: 'UDP', adress: '10030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'proxy(gse_btsvr)', type: 'agent', name: 'TCP,UDP', adress: '60020-60030', msg: this.$t('m.addSomeInfo.bt'), osSame: ''},
                    {port: 'agent', type: 'agent', name: 'TCP,UDP', adress: '60020-60030', msg: this.$t('m.addSomeInfo.bt'), osSame: this.$t('m.addSomeInfo.same')},
                    {port: 'agent', type: '', name: '', adress: this.$t('m.addSomeInfo.random'), msg: this.$t('m.addSomeInfo.btNone'), osSame: ''}
                ]
            }
        },
        watch: {
            'openStatus': function () {
                this.initApplications()
            },
            '$route': function () {
                this.showSvg = false
                this.showOpen = false
            }
        },
        computed: {
            menuList () {
                let menuList = this.$store.state.menuList
                for (let i = 0; i < menuList.length; i++) {
                    if (this.$route.path === '/') {
                        menuList[i].routerPath = 'stall'
                    } else {
                        menuList[i].routerPath = this.$route.path
                    }
                }
                return menuList
            },
            applications () {
                let apps = this.$store.state.stall.applications
                return apps
            },
            // 检测NGINX_SETTING_ERROR返回时显示的状态
            openStatus () {
                return this.$store.state.openDoor
            },
            appId () {
                return this.$store.state.stall.appliId
            }
        },
        mounted () {
            this.showSuperuser = window.is_superuser
        },
        methods: {
            clickflash () {
                clearInterval(this.$store.state.plug.timeTaskInfo)
                this.$emit('changeRouter')
            },
            appliId () {
                this.headName = window.user
                this.$store.dispatch('stall/getApplications').then(res => {
                    if (res.data.length) {
                        this.selectAppId = res.data[0].ApplicationID
                        this.$store.state.stall.appliId = res.data[0].ApplicationID
                    }
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            showChange () {
                this.showOpen = !this.showOpen
                if (this.showOpen) {
                    this.showSvg = false
                }
            },
            initApplications () {
                this.$store.dispatch('stall/getApplications')
            },
            // 改变表格形式
            changeNavbar (item, index) {
                this.indexNum = index
                if (this.indexNum === 0) {
                    this.tableInfo = this.agentGse
                }
                if (this.indexNum === 1) {
                    this.tableInfo = this.proxyGse
                }
                if (this.indexNum === 2) {
                    this.tableInfo = this.pagentGse
                }
            },
            // 获取当前的选中值
            getItem (index, data) {
                this.$store.commit('stall/changeAppliId', index)
                this.showOpen = false
                this.showSvg = false
            },
            svgShow () {
                this.showSvg = !this.showSvg
                if (this.showSvg) {
                    this.showOpen = false
                }
            },
            updatePlugin () {
                this.isPluginConfiging = true
                ajax.post(window.site + 'global_operate/init/', {}).then((res) => {
                    this.$bkMessage({
                        message: this.$t('m.nginx.configOk'),
                        theme: 'success'
                    })
                    this.showChange()
                    this.$store.commit('changeDoor')
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.isPluginConfiging = false
                })
            },
            // 更新Nginx配置
            updataInfo (keyInfo) {
                if (keyInfo === 'nginx') {
                    if (!(this.inputIntra)) {
                        this.$bkMessage({
                            message: this.$t('m.otherWord.complete'),
                            theme: 'error'
                        })
                        return
                    } else if (this.verify.isIntra || this.verify.isOuter) {
                        this.$bkMessage({
                            message: this.$t('m.otherWord.sureInfo'),
                            theme: 'error'
                        })
                        return
                    }
                } else if (keyInfo === 'timeout') {
                    if (this.timeOut < 600) {
                        this.verify.timeOut = true
                        return
                    } else {
                        this.verify.timeOut = false
                    }
                }
                
                let form = {}
                form.key = keyInfo
                if (keyInfo === 'nginx') {
                    form.inner_ip = this.inputIntra
                    form.outer_ip = this.inputOuter
                    this.isNginxSaving = true
                } else if (keyInfo === 'timeout') {
                    form.timeout = this.timeOut
                    this.isTimeSaving = true
                }
                ajax.post(window.site + 'config/kv/', form).then((res) => {
                    this.$bkMessage({
                        message: this.$t('m.nginx.save'),
                        theme: 'success'
                    })
                    this.showChange()
                    this.$store.commit('changeDoor')
                    this.getInfo()
                    this.appliId()
                }, res => {
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.isNginxSaving = false
                    this.isTimeSaving = false
                })
            },
            // 查询Nginx配置IP
            getInfo () {
                if (!this.appId) { return }
                ajax.get(window.site + 'config/kv/?key=nginx').then((res) => {
                    this.inputIntra = res.data.data.inner_ip
                    this.inputOuter = res.data.data.outer_ip
                }, res => {
                    this.inputIntra = ''
                    this.inputOuter = ''
                })
                ajax.get(window.site + 'config/kv/?key=timeout').then((res) => {
                    this.timeOut = res.data.data.timeout
                }, res => {
                    this.timeOut = ''
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
                ajax.get(window.site + 'config/kv/?key=plugin_config').then((res) => {
                    this.configTime = res.data.data.time
                }, res => {
                    this.configTime = ''
                    if (res.data.msg === '配置信息不存在，请先配置') {
                        return
                    }
                    this.$bkMessage({
                        message: res.data.msg,
                        theme: 'error'
                    })
                })
            },
            // 校验
            verifyInnerIp (type) {
                let reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\:([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-5]{2}[0-3][0-5])$/
                if (type === 'inner') {
                    if (reg.test(this.inputIntra)) {
                        this.verify.isIntra = false
                    } else {
                        this.verify.isIntra = true
                    }
                }
                if (type === 'outer') {
                    if (!this.inputOuter) {
                        this.verify.isOuter = false
                    } else {
                        if (reg.test(this.inputOuter)) {
                            this.verify.isOuter = false
                        } else {
                            this.verify.isOuter = true
                        }
                    }
                }
                if (type === 'time') {
                    if (this.timeOut < 600) {
                        this.verify.timeOut = true
                    } else {
                        this.verify.timeOut = false
                    }
                }
            }
        },
        created () {
            this.appliId()
        }
    }
</script>

<style lang="scss" scoped>
    @import '../scss/mixins/clearfix.scss';
    @import '../scss/mixins/scroller.scss';

    .bk-tab-change {
        padding-left: 2em;
        ul {
            @include clearfix;
            font-size: 14px;
            border: 1px solid #c3cdd7;
            width: 784px;
            border-bottom: none;
            li {
                width: 33.33%;
                border-right: 1px solid #c3cdd7;
                float: left;
                padding: 0 10px;
                line-height: 31px;
                cursor: pointer;
                color: #7b7d8a;
            }
            .bk-splice {
                border-right: none;
            }
            .bk-bord {
                color: #fff;
                background-color: #3c96ff;
            }
        }
    }
    .agent-header {
        font-size: 20px;
        z-index: 2000;
        box-sizing: border-box;
        width: 100%;
        min-width: 1280px;
        position: fixed;
        top: 0;
        left: 0;
    }
    .bk-agent {
        background-color: #313b4c;
        @include clearfix;
    }
    .bk-agent-logo {
        height: 50px;
        line-height: 50px;
        float: left;
        margin-left: 30px;
        > img {
            float: left;
        width: 37px;
        margin-top: 6px;
        }
        > p {
            float: left;
            color: #fff;
            font-size: 18px;
            margin-left: 10px;
        }
    }
    .bk-agent-navbar {
        font-size: 14px;
        margin-left: 64px;
        float: left;
        line-height: 50px;
        ul {
            @include clearfix;
            li {
                float: left;
                a {
                    padding: 0px 18px;
                    display: block;
                    color: #8292a7;
                    &.bk-click {
                        color: #bfcbda;
                        background-color: #283242;
                    }
                    &.bk-none-click {
                        color: #949494;
                    }
                }
            }
        }
    }
    .bk-import {
        background-color: #283242!important;
        .bk-icon {
            color: #bfcbda!important;
        }
        span {
            color: #bfcbda!important;
        }
    }
    .bk-agent-personal {
        float: right;
        @include clearfix;
        height: 50px;
        .bk-left {
            float: right;
            margin-right: 22px;
            height: 50px;
            line-height: 50px;
            cursor: pointer;
            padding: 0px 12px;
            @include clearfix;
            .bk-icon {
                font-size: 16px;
            }
            span {
                color: #8292a7;
                font-size: 14px;
            }
        }
        .bk-problem {
            margin-right: -5px;
        }
        .bk-center {
            float: right;
            @include clearfix;
            margin-top: 10px;
            .bk-selector-input {
                background: #283242;
                border: 1px solid #3b4658;
                .bk-selector-icon {
                    top: 12px!important;
                }
            }
        }
        .bk-right {
            float: right;
            height: 100%;
            margin-right: 35px;
            margin-left: 14px;
            line-height: 50px;
            .bk-img {
                float: left;
                overflow: hidden;
                width: 34px;
                height: 34px;
                border-radius: 50%;
                border: 1px solid #394456;
                margin-top: 8px;
                img {
                    width: 34px;
                    height: 34px;
                }
            }
            .bk-word {
                float: left;
                margin-left: 3px;
                span {
                    font-size: 14px;
                    color: #737987;
                }
            }
        }
    }
    .bk-open-change {
        /*position: fixed;
        top: 50px;
        left: 0;
        z-index: 20;
        @include clearfix;
        width: 100%;
        background-color: #ffffff;
        border-bottom: 1px solid #dde4eb;
        padding-top: 25px;
        overflow: auto;
        @include scroller(#fff);
        height: 100%;
        padding-bottom: 50px;*/
        width: 100%;
        height: calc(100% - 50px);
        background-color: #fafbfd;
        position: fixed;
        top: 50px;
        left: 0;
        z-index: 10;
        min-width: 1180px;
        overflow: hidden;
    }
    /*.bk-open-shade {
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
        position: fixed;
        top: 600px;
        left: 0;
        z-index: 999;
        min-width: 1180px;
    }*/

    .bk-stall-change {
        width: 100%;
        .bk-ip-info {
            background: #f1f5fa;
            padding: 20px 54px;
            margin: 0 auto; 
            width: 1020px;
            height: 128px;
            > p {
                font-size: 14px;
                color: #737987;
                line-height: 20px;
            }
            .bk-p-gray {
                color: #999;
            }
            .bk-p-black {
                color: #333;
                padding-bottom: 8px;
            }
        }
        .bk-change-ip {
            float: left;
            overflow: hidden;
            text-align: center;
            .bk-form-item {
                width: 400px;
                float: left;
                .bk-label {
                    float: left;
                    line-height: 36px;
                    font-size: 14px;
                    color: #737987;
                }
                .bk-form-content {
                    float: left;
                    input {
                        width: 310px;
                        height: 36px;
                    }
                }
                &.bk-ip {
                    margin-top: 18px;
                }
                &.ml55 {
                    margin-left: 55px;
                }
            }
        }
        .bk-change-btn {
            float: right;
            overflow: hidden;
            margin-top: 18px;
            button {
                width: 100px;
                height: 36px;
            }
        }
    }
    /*
    ** 配置Nginx Server
    */
    .bk-stall-ip {
        .bk-stall-change {
            /*height: 92px;*/
            background-color: #ffffff;
            border-bottom: 1px solid #dde4eb;
            overflow: hidden;
            position: fixed;
            top: 50px;
            left: 0px;
            width: 100%;
            .bk-change-ip {
                float: left;
                overflow: hidden;
                text-align: center;
                position: relative;
                .bk-form-item {
                    width: 380px;
                    float: left;
                    .bk-label {
                        float: left;
                        line-height: 36px;
                        font-size: 14px;
                        color: #737987;
                    }
                    .bk-form-content {
                        float: left;
                        input {
                            width: 310px;
                            height: 36px;
                        }
                    }
                    &.bk-ip {
                        margin-top: 27px;
                    }
                    &.ml55 {
                        margin-left: 55px;
                    }
                }
            }
            .bk-time-out {
                height: 36px;
            }
            .bk-change-btn {
                float: left;
                overflow: hidden;
                margin-top: 27px;
                button {
                    width: 100px;
                    height: 36px;
                }
            }
        }
        .bk-content {
            text-align: center;
            width: 100%;
            background-color: #fafbfd;
            p {
                font-size: 22px;
                color: #333c48;
                margin: 0;
                padding: 0;
                padding-top: 151px;
            }
            .bk-btn {
                padding-top: 54px;
                button {
                    width: 151px;
                    height: 42px;
                }
            }
        }
    }
    .bk-input-checked {
        border-color: #ff6600 !important;
    }
    .bk-svg-shade {
        width: 100%;
        height: 100%;
        background-color: #fff;
        position: fixed;
        top: 50px;
        left: 0;
        z-index: 10;
        min-width: 1180px;
        overflow: hidden;
        .bk-svg {
            height: 100%;
            padding: 20px 0;
            overflow: auto;
            @include scroller(#fff);
        }
    }
    .bk-svg-img {
        width: 1112px;
        margin: 0 auto;
    }
    .bk-svg-info {
        background: #f1f5fa;
        margin: 0 auto;
        margin-top: 30px;
        margin-bottom: 80px;
        padding: 20px 54px;
        width: 1112px;
        > p {
            font-size: 14px;
            color: #737987;
            line-height: 25px;
        }
        .bk-p-gray {
            color: #999;
            padding-left: 4em;
        }
        .bk-indent {
            text-indent: 2em;
        }
        .bk-p-black {
            color: #333;
            padding-bottom: 8px;
        }
        .bk-black-ml {
            margin-top: 10px;
        }
    }
    .bj-svg-step,
    .bj-svg-table {
        > p {
            font-size: 14px;
            color: #737987;
            line-height: 20px;
            .bk-round {
                font-size: 20px;
                font-weight: 700;
            }
        }
    }
    .bj-svg-table {
        .bk-tab-svg {
            padding: 8px 0;
            height: 444px;
        }
        table {
            margin-left: 2em;
            width: 784px;
            border: 1px solid #c3cdd7;
            border-bottom: none;
            -webkit-border-horizontal-spacing: 0px;
            -webkit-border-vertical-spacing: 0px;
            th {
                padding: 0px 10px;
                height: 30px;
                line-height: 30px;
                color: #333;
                font-size: 14px;
                border-bottom: 1px solid #c3cdd7;
                text-align: left;
                overflow: hidden;
                box-sizing: border-box;
            }
            td {
                line-height: 25px;
                height: 25px;
                border-bottom: 1px solid #c3cdd7;
                font-size: 12px;
                padding: 0px 10px;
            }
        }
    }
    
    .bk-splice-splice {
        margin: 0 auto; 
        width: 1020px; 
        padding-bottom: 30px; 
        overflow: hidden;
        position: relative;
    }
    .bk-splice-line {
        position: absolute;
        top: 63px;
        left: 0;
        width: 100%;
        height: 1px;
        background-color: #c3cdd7;
    }
    .bk-stall-margin {
        height: 100%;
        height: 20px;
        background-color: #f1f5fa;
    }
</style>
