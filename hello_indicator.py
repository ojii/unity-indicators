import gobject
import gtk
import appindicator

if __name__ == "__main__":
    ind = appindicator.Indicator ("example-simple-client",
                                  "indicator-messages",
                                  appindicator.CATEGORY_APPLICATION_STATUS)
    ind.set_status (appindicator.STATUS_ACTIVE)
    ind.set_label("Hello")

    # create a menu
    menu = gtk.Menu()

    # create some 
    menu_items = gtk.MenuItem("World!")

    menu.append(menu_items)

    menu_items.show()

    ind.set_menu(menu)

    gtk.main()
