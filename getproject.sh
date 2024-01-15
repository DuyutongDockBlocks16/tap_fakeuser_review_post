unzip simuLogin.zip
rm simuLogin.zip -rf
cd MultiTaptapAppsReviewGet/
cp -r ./node_modules ../simuLogin/
cd ..
cd simuLogin/
cnpm install commander
