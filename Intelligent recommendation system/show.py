import os
import sys
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

fonts = ["PingFang_Bold.ttf", "PingFang_ExtraLight.ttf", "PingFang_Heavy.ttf", "PingFang_Light.ttf", "PingFang_Medium.ttf", "PingFang_Regular_0.ttf"]
image = ["princess.png"]

image_path = os.path.join(sys.path[0], "image")
fonts_path = os.path.join(sys.path[0], "fonts")


def img_generate(text, out_file):
    mask = plt.imread(os.path.join(image_path, image[0]))*255
    print(mask.shape)
    txt = " ".join(text)
    word = WordCloud(background_color="white",
                   font_path=os.path.join(fonts_path, fonts[4]),
                   mask=mask,
                   ).generate(txt)
    image_colors = ImageColorGenerator(mask)
    #word = word.recolor(color_func=image_colors)
    save_path = os.path.join(sys.path[0], 'save')
    os.makedirs(save_path, exist_ok=True)
    word.to_file(os.path.join(save_path, out_file))  #bao
    print("词云图片已保存")
    #plt.imshow(word)
    #plt.axis("off")


if __name__ == "__main__":
    text = ["你好吗", "我很好", "樱花", "幸运", "成功", "加油", "好棒", "真心", "手机", "信息", "苹方", "公主", "水杯", "蛋糕"]
    img_generate(text, "output.png")
